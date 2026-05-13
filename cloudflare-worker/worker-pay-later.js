/**
 * Rogue Night — Pay Later Worker
 *
 * Receives POST /api/pay-later with { email, name, business, ref }
 * Creates a Stripe customer + $350 invoice with collection_method=send_invoice
 * Stripe automatically emails the customer the Hosted Invoice Page link.
 *
 * Required Worker secrets:
 *   STRIPE_SECRET_KEY     — Stripe live (sk_live_...) or test (sk_test_...) secret
 *   ALLOWED_ORIGIN        — e.g. "https://roguenight.com.au" (single origin)
 *
 * Required env (vars, plain text):
 *   PRODUCT_NAME          — default "Digital Health Check"
 *   AMOUNT_CENTS          — default 35000 (A$350.00)
 *   CURRENCY              — default "aud"
 *   DAYS_UNTIL_DUE        — default 14
 *
 * Deploy: see /agent/workspace/cloudflare-worker-setup.md (walkthrough)
 *
 * Voice rules baked in:
 *   - Customer description uses "small to medium businesses" voice (no SME)
 *   - Invoice description: "Digital Health Check — specially curated report"
 */

const ALLOWED_METHODS = "POST, OPTIONS";
const ALLOWED_HEADERS = "Content-Type";

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": ALLOWED_METHODS,
    "Access-Control-Allow-Headers": ALLOWED_HEADERS,
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin),
    },
  });
}

// Encode body to application/x-www-form-urlencoded for Stripe API.
function form(params, prefix) {
  const parts = [];
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null) continue;
    const key = prefix ? `${prefix}[${k}]` : k;
    parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(v))}`);
  }
  return parts.join("&");
}

async function stripeCall(env, path, body, idempotencyKey) {
  const headers = {
    "Authorization": `Bearer ${env.STRIPE_SECRET_KEY}`,
    "Content-Type": "application/x-www-form-urlencoded",
    "Stripe-Version": "2024-06-20",
  };
  if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  const resp = await fetch(`https://api.stripe.com/v1${path}`, {
    method: "POST",
    headers,
    body,
  });
  const data = await resp.json();
  if (!resp.ok) {
    const msg = data && data.error && data.error.message ? data.error.message : `Stripe ${resp.status}`;
    throw new Error(msg);
  }
  return data;
}

function isValidEmail(email) {
  if (!email || typeof email !== "string") return false;
  // Lightweight check; Stripe will reject malformed addresses on its side.
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function handlePayLater(request, env) {
  const origin = request.headers.get("Origin") || env.ALLOWED_ORIGIN || "*";
  // Optional: enforce strict origin match
  if (env.ALLOWED_ORIGIN && origin !== env.ALLOWED_ORIGIN) {
    return json({ error: "Origin not allowed" }, 403, env.ALLOWED_ORIGIN);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ error: "Invalid JSON" }, 400, origin);
  }

  const email = (body.email || "").trim().toLowerCase();
  const name = (body.name || "").trim();
  const business = (body.business || "").trim();
  const ref = (body.ref || "").trim();

  if (!isValidEmail(email)) {
    return json({ error: "A valid email is required." }, 400, origin);
  }

  const productName = env.PRODUCT_NAME || "Digital Health Check";
  const amountCents = parseInt(env.AMOUNT_CENTS || "35000", 10);
  const currency = (env.CURRENCY || "aud").toLowerCase();
  const daysUntilDue = parseInt(env.DAYS_UNTIL_DUE || "14", 10);

  // Idempotency key derived from Tally submission ref (if provided) + email + day.
  // Prevents accidental double-clicks creating duplicate invoices.
  const dayBucket = new Date().toISOString().slice(0, 10);
  const idemKey = `dhc-${ref || email}-${dayBucket}`;

  try {
    // 1. Create or update customer (Stripe upserts by email when using a known ID is impractical;
    //    we create a fresh one per submission and rely on Stripe Dashboard dedupe in practice).
    const customerBody = form({
      email,
      name: name || business || email,
      description: business
        ? `${business} — Digital Health Check customer (small to medium business)`
        : "Digital Health Check customer (small to medium business)",
      "metadata[tally_ref]": ref || "",
      "metadata[business]": business || "",
      "metadata[source]": "thank-you-page-pay-later",
    });
    const customer = await stripeCall(env, "/customers", customerBody, `${idemKey}-customer`);

    // 2. Create the invoice item (line item, attached to the customer, will be pulled into next invoice).
    const itemBody = form({
      customer: customer.id,
      amount: amountCents,
      currency,
      description: `${productName} — specially curated report for ${business || email}`,
    });
    await stripeCall(env, "/invoiceitems", itemBody, `${idemKey}-item`);

    // 3. Create the invoice. collection_method=send_invoice + auto_advance=true
    //    tells Stripe to finalize and email the Hosted Invoice Page link automatically.
    //    pending_invoice_items_behavior=include pulls the pending invoice item we just
    //    created in step 2 into this invoice. Stripe's default is `exclude` (since 2024),
    //    which would create an empty $0 invoice. Always set this explicitly.
    const invoiceBody = form({
      customer: customer.id,
      collection_method: "send_invoice",
      days_until_due: daysUntilDue,
      auto_advance: "true",
      pending_invoice_items_behavior: "include",
      description: `Digital Health Check — your specially curated report. Pay any time within ${daysUntilDue} days. Report begins once invoice is paid.`,
      "metadata[tally_ref]": ref || "",
      "metadata[source]": "thank-you-page-pay-later",
    });
    const invoice = await stripeCall(env, "/invoices", invoiceBody, `${idemKey}-invoice`);

    return json({
      ok: true,
      invoice_id: invoice.id,
      hosted_invoice_url: invoice.hosted_invoice_url || null,
      status: invoice.status,
      customer_id: customer.id,
    }, 200, origin);

  } catch (err) {
    // Log to Worker console; respond with a customer-safe message.
    console.error("Pay later error:", err && err.message ? err.message : err);
    return json({
      error: "We couldn't create the invoice automatically. Please email hello@roguenight.com.au and we'll send it manually.",
      debug: env.DEBUG ? String(err && err.message ? err.message : err) : undefined,
    }, 500, origin);
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || env.ALLOWED_ORIGIN || "*";

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname === "/api/pay-later" && request.method === "POST") {
      return handlePayLater(request, env);
    }

    // Lightweight health check
    if (url.pathname === "/api/health") {
      return json({ ok: true, worker: "rogue-night-pay-later" }, 200, origin);
    }

    return json({ error: "Not found" }, 404, origin);
  },
};
