"""Asset loading for populate_template.

Holds the inline base64 avatar PNGs used by Section 02 (workflow steps),
plus the `_resolve` helper for locating data files in either the repo
layout (data files in a sibling `data/` directory) or the Hyperagent
skill workspace layout (data files alongside the scripts).

Why inline-base64 avatars? Hyperagent's PublishWebpage sandbox cannot
authenticate against /api/files/ URLs, so any image must be embedded
directly. See the brand kit memory and the embed_images.py pattern.
"""
from pathlib import Path

SKILL_DIR = Path(__file__).parent
# Two candidate data directories cover both layouts:
# - When the script lives in `agents/dhc-report-writer/scripts/`, data is at `../data/`
# - When the script lives in `agents/dhc-report-writer/` (or flat skill workspace),
#   data is at `./data/`
DATA_DIR = SKILL_DIR.parent / "data"
LOCAL_DATA_DIR = SKILL_DIR / "data"


# ---------------------------------------------------------------------------
# Workflow avatar illustrations (Style C — editorial spot illustrations,
# 48×48px PNG base64). Used in Section 02 day-in-the-life rows and other
# "who does this" callouts.
# ---------------------------------------------------------------------------
AVATAR_AGENT_B64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAAQeElEQVR42pVZaZQcV3W+775XXb1Md4961h5Jo9HIkiyNJFvGlpWAiY+NsSzjneQEkvDDWIsNxjjkEIM5JIcl7MZ4iWVESALkcHIAI2E5Ng4QQiDGErKwbElI1ghJ1mw9M71OL1X13rv58ap6RjLkJPVDp2rUVe97d/3u95CZGRZe7SfE6M4Yw8xCCPt4/PiJ/S/uP3To5dHR0cmJqUql0mp5iCCEyGQy+YH86tWrNl526VWbLr949Wr7itYaEYlowQLzCy1cHs0FeM7/FTMbYyyUsbGxvXuffu7Z548ePVYpV5jZcRwhhBQCiSzuIAiCILCvZDKZkZE1N2zdctNNNy5estjCIiJEXAjnfGvw7wVkFxBEADA6euqJv39y754fTE1Nx2JOMpmUUoZ4AZjZrgGRse2j1rrVanktr7ev55Zbb777nh0rVgzbzxLR/xHQ/L3WWgrped7DX35k1xO7S6VSR7rDjbnGGGYT/hZDUzIzIgAgM4f3jEiIiAjgB0G1Ws115e6+e/sH7/+A67pKKyHkQm/w73cZA4PWWkp5+PAr99/3V786cDDbmZVSaq0tCrsMAzMAArIxbNcHsF+LfgDAYNgAgBBCBUGpXL5y8xUPP/zQhkvWK6WElPgGY6AxDBhuFphD20j5ve99/0P3f7jZbGYyGaWUjWuECA/PGyh0FAMDMxsEQgRAtICN0RY3AEtHVqu1RCLxlUceuuOdt1lM8/EKAMDUNv28p6TctWv3zu3vA4BMJq2Uig5Rxhgi2A8GgUaIQggppX0FAOzdgmEYAhCRwAB7iAjU3FqACGGv2RJiwAB7iLDXAQDsr0KIRkTbGu0lhPYS9o3sJSwiAEKEQAS0F9oFgkAEALJP2QPBLodfBwAQGUMA+xpEhPYS9hAJgIDsBdoFANs5BeyJgKxr2c9si/aB7Yvti9oNAGyzbXP2lwBoXwT2DewKEbU/Yv9wKbS3sm/cMtgPiwj7jACEf/+H/PoXMowxgSU6BSx+9pEdkAlJYESuawWAEAJYpZBhhMRBJATL2EJREguIENGwoSJZpiowJDIVwSXSWPxnyAWuMNAtcoVQUSGEbHKVA5n2HZ4kAhFXJYJpaQpWZTHsa4n6JpyKQVcZNlhgmsyZwBgaIJagMQzGYIyq2D0Cw3+lJEbDzaJsxhRRkrjnsxnTRJZHJYn2Tx7g8r/m/9D5W+P6Z9j/9D1eY8sP6/o9Hb6kxAAAAAElFTkSuQmCC"

AVATAR_YOU_B64 = "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"

AVATAR_TEAM_B64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAASgUlEQVR42m1ZWZBcZ3U+5//vfm9v092zz2ik0WhkbZaxhLUZyQRjsAkYUpgHqpIKVFGkUslLwkNeUqSoCpVKeEpRKSqhoCqAwY5TgLFxiME2kpFkWWizNFpmpNm3nqV7uu/+///JQ3fPSCK3+qHv7b73nPud/Tv49Nc+BYAABIAAAEDQPiFoHQwREaM0idLENa2hcve+gaHRnsHBjs6il3UMizNEZEqpRhytNmozq5VbizPXZyfvLi/4cWTphm0Yikgp2nwuQlvg5tG8/vTX/njr7IEDAQgBkWGUJqkUQ6Wuj4weOLJzz1Cpy7McAJCklCJFiggQARAZMs6YxjgBNKJgamXp7Pj1d25enaws6lyzDEMREVFbGWoLamtETYVw6xwQN39lDIWUfhyO9gy88MRTJ0b3Zx1PShGniVSKiJrIbd3SvI8AgIiIM2bqBte0euD/9ubVl8+/c2txxjUtjXOlVOuvLaBoU2hboaah7ns0Z6wRhRnL/uLxjz3/+AnXNIM4FkohACIgPKjHlsEJEal93sRDY9yxLD+Ofnrh9H+++6Yfh55pSyW3fGTLWYAPHx99wEwIAMCRbYT+wW3D3/j8l0/ueUyINEgSIOKMNTEB2MQSgYBxJoUAIMY5bUkARMYQgShOE4bs8eHdx0b23l1auFdZcAyr5UuIQEDYMt79CrXgY4gbQfD8oeN//9k/LTiZRhgCAkcGAIgIyFrymighEFESRiKVSkEShaZlk6Km1kjNW1ovGsZhOZP7+P7DG1FwaeqOrRv3i24+/0GEEBDRj8I/P/mJv3rms4kQiRCcM2w6OGOADGBLDgEBQBpFcRT76/ONtSXdyigpdMsiok2ztr4gcsYSIQDh1J7HGOK5iTFD04m2QgoR+Y7jo5tuzBhrROFXnnr2Sx99rh4EAMQYwoMG2vSc5msTqSQWjdWpvF5xuF+t+nqmrGmcMU7QDiiGm5gyxhRBnCRHRvcB0dk7N2zDbP6t+VQGQAQEQJyxmu9/7tCJPzv5yXqjgU2RdF8stMKniX/zElNCSqkYxWuV9aWFVc4lKWqFCNe0WDMbD72V3+9vRYW4UdCkSO7c4IK5cE3H/g3eP3FisVP04MXWN69ry3WtWOhNJZPINKlSO7c4IK5cE3H/g3eP3FisVP04MXWN69ry3WtWOjRIUetaIQZpAmQEWLsb3+u/vlMm+lGxk0p/KDqFEKNJvRSKca+LIfmSBBHKoYUGlhqsVE0dN3gShKoXJXCVVN5f+zb5+b+/eI5XVU4Y7EUp4YPxBnGOJdKzK9Orywvnbp2+eTAYZu1FNFxnYbfUPuBpw70dW5dqFepSwRfDhiupvJRE5L65HWxmGGz/V2JCfp3zyPIRHBwcfh+v334VJv7h8ZnWHJKsCGt0HN0T8g5J9pKJGPbdNp7Y9C1K1i9EMXEzHh8YFiL5ZqO78r6oLKf1FYCJLLuqlK+Fk3FU0pJdMfD0FNSI8MAQnKyOuGqmpqCZKFOsRCJCGMIIlQ5r5hXLQsKWQYhLquh0GI2Hgex6xW7U8FhslmVSmHYawZe+P6jGN3kPJEO74IKUWA4HtONp3Xq4k1bJ4pRSx+2M99qWa7vqdbemGWZeIBEqI8elcFwbJllZqJUyXFSnZCBUGSE+0YMN2y3W8bSceJ5OVa3bZUFSCNJJIkW/nALj3wkbSs0ulkh+KyGLjGkNQJKN0a3M3tXbnFV03NI0x5rieYeqcc8cLGm4riMh1fMMw4paZsv1USjcNzXECxjQhRMxUKivLcRLqvKNHIz0L6qD5PmKxjIj/43//VyGbA4W6ycW1lnacNjnZjEZEDAULIQ8MV1bvLCdxy0t8x9UOcjHG0EAp7bj20IGOI3s3cJKxIcb5+FGLprN61I+b4fRp03GhMBAO4Z8dqePVP9v7YGM5y1BbcjcGfebz93s3qNaYz37yHkiiGK/EfmOFyAQEDmtJkqT0nfDNPR0yzHM+h9+NJpQAAiB3TMkgJAREBAyVkKcOHPFLUbzA23fQIiLJm6ZHdMeqWNd9bFh0R/AjqOyTjWzduJ3uxRBLKc0t2HJ2RkHbZIhIkCLleFpSC7wOVWs31prmU7mtm+bJ4Z7cUjVMAxoSlKqb6VExIxopEYjIQ0t2P3K+cOVkEFqmMlEsJUmj4yXR3N5VIkUn9IDKVHDSRKn+3r2Lk4urE2qoMmR9xojh0EsG/FiilwIFxn1X2pXaObzx+YBJBEkGgAD0SOdZYrcoKYMR5RmJL+VKg94fCaW7InTRJGKk0TjHJCFcRwHoSRAuqkCYH9v+dCJZ4Wsl7Qy19ixTX+4OKv/1VdXaJjh8KA0lI6C5v/nZn/2HhVxXaHDSbJekRISlWxhNO0n9dqz6hxzjcxB6gcKr9oKdaTK1kcgmqJJHRYqUyWZf1Qp7xbJBSgMC6YqVIIhIZ8qMY1Gb3p0vWkIp7sIgQhRYSuqK/52Gy1uVpM6T/QNdq2IenqyIQvicl2MjktWVxYfB8G7G4zhDNdjgicMCNp6S5zy0F8JlvY3MK/kM2H4wPgd+0/Oy+29bnp+6xqNNuN5H4ABpzd+xI5c5J9uSNTM13a6k80m3Z/pO8bNbqy/r5aVVAK2tzVdqXr3u/vaHv3H7jU9qpotJ0LTnFigBAKDGS3vTVR8gvYi9lj5U6JQnNRmqSSw9kT54UmzalFKtKEm9cjI3q/vDq2L+R2hpCJhI4FaqfR2pWP5BtRqaUfVLpR76sSJm7aRNiw0LoGiJfSKfhQJCsNQ/x3WROeIFn0CKCBJRQ+cQfVhk2xJ+3dOjk8Oqzv7vSWVh0yYm+2t/Ly8qvP7zt5G5w3V8uCW5OYBGjLMFJr8kfBtjOMz1NqsVhf3Y/sA4uNdG7JEHDKVHCZiRDJIKuXt0uc9mSlq3rjBIk8ZLAQW2hOh2EVlffUMOb4tqq6lhJNTJMpBDN6FvsBxYqnf2JVi2W+4Gxb/3HhwnmIkwTOQ+IZVkCElC24H2C0gxcfSoZqKA9RL5oeRCF69Y1fWVnTWzX8k8v/wfRUGJHCh5Lh3+4gRo84NiO3oC6Xg+VHKk3F7KlqIIJO9gCgGLdDHoFb2WxOE9N29dqb+w60ksU4sTBTKBbK5KaEkGVn2A1Vcp7IZ5IRLlGpZ4oOiQlRw/d3c/7Q6NjA4Gvut7i7NLLFz1nEsC5bJFw4qB4ZEwmgC5ubmxKevYM++f0pA8lzjmF8fDpMxDjPB3E6ydW2lUmjIKXRt8P7i8OBXIOvGXLfaRRX3dkP5kcAYApNfKdPk3Tp1ZhMrNnSwN7RYwR9d2Tf5cUbzK8utRYQFbK5bEcv06TcsPYITHBD+sVkT2eFu+Ou7OzCw38EBHREuX+3t75aRg7nAVhMMOw1H9Mb4+Ng/M+X/20fTYKuTQcxSZUPpGqlPThfO3FlSHM2kl3vF8KT2x5x9uZXzU71/d8+Hx4+WC/2uYzmOaxV1ICRCCaanrFz/h1efP+8FWNbFLAQZqSIEkFRFVR3N2KDa/4VUvw1mEYekHlxr6eeAyGxLBNRFpcJsZ5MKmGYdpSn7sGi3Gv7Cqv5P9OW+YdaFcY3LOy7LnfFzA8PGpqQSTYuJCJSECghPDe5fOY/Tj9+sJWxSSqRhN4f3FueuKMoqq5g1t2bPjFJCJBJmqBQ3j/khnE50LqS5XMupO+FUq1cLi3D5vdJXaHv7eKH2kxSTGdpzzw9U1SVJJ4jhlq/fXCqUy59dcfVnv5w37AQAE1Jyg8/fmLlRmbw3N3dsZE+38+CsAf9JqpWaVzTN3O3+mXsj08rjBp6+YkL0VjvbcaKm7IJ9u/90Oeg18Pw2RTd8RL1KvtbhJaX8OGGYJjdJLnAJx3sVQdqYVBJuxPEd01CJ6h1A0i30k+tg3slwujJPcbgk5UrCm+8e9c3l+6mIvIjFEGLSqO9HyRhYGp8fXm1b99RK+w60bZ0g2DKv4TIf+7avYBrB/UmMhbJJJGiZT6U2kY5E2H1UMhU0dCODJMpBDN6FvsBxYqnf2JVi2W+4Gxb/3HhwnmIkwTOQ+IZVkCElC24H2C0gxcfSoZqKA9RL5oeRCF69Y1fWVnTWzX8k8v/wfRUGJHCh5Lh3+4gRo84NiO3oC6Xg+VHKk3F7KlqIIJO9gCgGLdDHoFb2WxOE9N29dqb+w60ksU4sTBTKBbK5KaE="


def _resolve(filename):
    """Resolve a data file's path. Handles three layouts:

    - Repo layout with scripts/: data files in `agents/dhc-report-writer/data/`,
      accessed via `../data/{filename}` from the scripts/ subdir.
    - Repo layout without scripts/: data files in `agents/dhc-report-writer/data/`,
      accessed via `./data/{filename}` from the package directory.
    - Hyperagent skill workspace layout: all files flat in
      `/agent/workspace/skills/{skillName}/`, so the script directory itself
      contains the data files.

    Returns the first existing path, or None if not found anywhere.
    """
    for candidate in (DATA_DIR / filename, LOCAL_DATA_DIR / filename, SKILL_DIR / filename):
        if candidate.exists():
            return candidate
    return None


def load_style_block() -> str:
    """Read the v5 style block from `v5-style-block.txt`.

    Returns a placeholder `<style>` comment when the file is missing so the
    render doesn't crash — the report just renders unstyled until the file
    is staged.
    """
    style_path = _resolve("v5-style-block.txt")
    if style_path:
        return style_path.read_text()
    return "<style>/* v5-style-block.txt not staged — render will be unstyled. Copy from the v5 reference template before running. */</style>"


def load_logo_b64() -> str:
    """Read the horizontal lockup PNG base64 for the cover.

    Returns empty string if missing — cover image will be broken but the
    rest of the render proceeds.
    """
    logo_path = _resolve("horizontal-b64.txt")
    if logo_path:
        return logo_path.read_text().strip()
    return ""


def load_extra_styles() -> str:
    """Read the additional CSS block (extra-styles.css) that styles
    report-specific elements not covered by v5-style-block.txt — phase
    headings, batch cards, agent cards, workflow tables, day-in-the-life
    comparison table, security assurance grid, tier summaries, etc.

    Returns a placeholder comment if the file is missing.
    """
    css_path = _resolve("extra-styles.css")
    if css_path:
        return css_path.read_text()
    return "/* extra-styles.css not staged — report-specific styling absent */"
