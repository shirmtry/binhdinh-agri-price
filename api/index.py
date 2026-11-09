# -*- coding: utf-8 -*-
"""Bảng giá nông sản Bình Định 2026 – lúa, sắn, tiêu, điều và 6 loại khác.
Tác giả: HTK · Hotline/Zalo: 0396241674 · Email: htk.contact@gmail.com
Cập nhật: 09/11/2026
"""
import os
import random
from datetime import date, timedelta

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

_fastapi = FastAPI(
    title="Bảng giá nông sản Bình Định 2026", docs_url=None, redoc_url=None
)
_fastapi.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
_fastapi.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

NOTE = "Dữ liệu mô phỏng – cập nhật 09/11/2026"
UPDATED_AT = "09/11/2026 08:00"
TODAY = date(2026, 11, 9)
CONTACT = {
    "author": "HTK",
    "hotline": "0396241674",
    "zalo": "https://zalo.me/0396241674",
    "email": "htk.contact@gmail.com",
}

# Dữ liệu mô phỏng – cập nhật 09/11/2026
# Giá tham chiếu VNĐ/kg cuối 2026 sau mùa mưa lũ: vận chuyển khó, thương lái ép giá.
PRODUCTS = [
    {"id": "lua", "name": "Lúa", "base": 7800,
     "context": "Lúa Thu Đông ngập úng ở Tuy Phước, An Nhơn; giá lúa tươi giảm do độ ẩm cao."},
    {"id": "san", "name": "Sắn (mì)", "base": 4200,
     "context": "Sắn vùng Tây Sơn, Vĩnh Thạnh thu hoạch chạy lũ, thương lái ép giá củ tươi."},
    {"id": "tieu", "name": "Tiêu", "base": 145000,
     "context": "Tiêu khô giữ giá tốt nhưng chi phí vận chuyển sau bão tăng."},
    {"id": "dieu", "name": "Điều", "base": 26000,
     "context": "Điều thô Phù Cát, Hoài Ân mất mùa vì mưa trái mùa, giá nhích nhẹ."},
    {"id": "bap", "name": "Bắp", "base": 6500,
     "context": "Bắp nếp bán chạy dịp cuối năm, nguồn cung từ Phù Mỹ ổn định."},
    {"id": "dau-phong", "name": "Đậu phộng", "base": 28000,
     "context": "Đậu phộng Đức Thọ (Phù Cát) phơi khó trong mưa, hàng khô khan hiếm."},
    {"id": "me", "name": "Mè", "base": 42000,
     "context": "Mè Hoài Ân, An Lão ít hàng sau lũ, giá tăng đều."},
    {"id": "khoai-lang", "name": "Khoai lang", "base": 12000,
     "context": "Khoai lang Tuy Phước ngập nước, củ xấu bị loại nhiều."},
    {"id": "mia", "name": "Mía", "base": 1400,
     "context": "Mía nguyên liệu An Nhơn thu hoạch sớm chạy lũ sông Kôn."},
    {"id": "dau-xanh", "name": "Đậu xanh", "base": 34000,
     "context": "Đậu xanh đãi vỏ cung cấp chợ Quy Nhơn, giá ổn định."},
]
PRODUCT_MAP = {p["id"]: p for p in PRODUCTS}

DISTRICTS = [
    "Quy Nhơn", "An Nhơn", "Tuy Phước", "Phù Cát", "Phù Mỹ", "Hoài Nhơn",
    "Hoài Ân", "Vĩnh Thạnh", "Tây Sơn", "An Lão", "Vân Canh",
]
# Hệ số giá theo huyện: xa trung tâm / đường sạt lở sau bão => chênh lệch mạnh hơn.
DISTRICT_FACTOR = {
    "Quy Nhơn": 1.05, "An Nhơn": 1.00, "Tuy Phước": 0.95, "Phù Cát": 0.98,
    "Phù Mỹ": 0.97, "Hoài Nhơn": 1.02, "Hoài Ân": 0.93, "Vĩnh Thạnh": 0.90,
    "Tây Sơn": 0.92, "An Lão": 0.88, "Vân Canh": 0.89,
}


def _rng(seed_text):
    return random.Random("htk-2026-" + seed_text)


def trend_prices(product_id, days=30):
    """Chuỗi giá 30 ngày kết thúc đúng giá hiện tại (random walk có seed cố định)."""
    p = PRODUCT_MAP[product_id]
    rng = _rng("trend-" + product_id)
    prices = [p["base"]]
    for _ in range(days - 1):
        drift = rng.uniform(-0.018, 0.02)
        prices.insert(0, max(500, round(prices[0] * (1 - drift))))
    prices[-1] = p["base"]
    return prices


def current_prices():
    out = []
    for p in PRODUCTS:
        series = trend_prices(p["id"])
        prev = series[-2]
        change_pct = round((p["base"] - prev) / prev * 100, 1)
        out.append({
            "id": p["id"],
            "name": p["name"],
            "unit": "VNĐ/kg",
            "price": p["base"],
            "changePct": change_pct,
            "context": p["context"],
        })
    return out


def district_prices(product_id):
    p = PRODUCT_MAP[product_id]
    rows = []
    for d in DISTRICTS:
        rng = _rng("district-" + product_id + "-" + d)
        price = round(p["base"] * DISTRICT_FACTOR[d] * rng.uniform(0.97, 1.03) / 50) * 50
        rows.append({
            "district": d,
            "price": price,
            "diffPct": round((price - p["base"]) / p["base"] * 100, 1),
        })
    return rows


def page(name):
    return FileResponse(os.path.join(TEMPLATES_DIR, name), media_type="text/html")


@_fastapi.get("/", response_class=HTMLResponse)
def home():
    return page("index.html")


@_fastapi.get("/bang-gia", response_class=HTMLResponse)
def bang_gia():
    return page("bang-gia.html")


@_fastapi.get("/about", response_class=HTMLResponse)
def about():
    return page("about.html")


@_fastapi.get("/api/prices")
def api_prices():
    return JSONResponse({
        "province": "Bình Định",
        "note": NOTE,
        "updatedAt": UPDATED_AT,
        "unit": "VNĐ/kg",
        "contact": CONTACT,
        "products": current_prices(),
    })


@_fastapi.get("/api/trend")
def api_trend(product: str = "lua"):
    if product not in PRODUCT_MAP:
        return JSONResponse({"error": "Không tìm thấy loại nông sản"}, status_code=404)
    prices = trend_prices(product)
    labels = [(TODAY - timedelta(days=29 - i)).strftime("%d/%m") for i in range(30)]
    return JSONResponse({
        "note": NOTE,
        "product": PRODUCT_MAP[product]["name"],
        "productId": product,
        "unit": "VNĐ/kg",
        "labels": labels,
        "prices": prices,
    })


@_fastapi.get("/api/by-district")
def api_by_district(product: str = "lua"):
    if product not in PRODUCT_MAP:
        return JSONResponse({"error": "Không tìm thấy loại nông sản"}, status_code=404)
    return JSONResponse({
        "note": NOTE,
        "product": PRODUCT_MAP[product]["name"],
        "productId": product,
        "unit": "VNĐ/kg",
        "districts": district_prices(product),
    })


@_fastapi.exception_handler(404)
async def not_found(request: Request, exc):
    path = os.path.join(TEMPLATES_DIR, "404.html")
    if os.path.isfile(path):
        return FileResponse(path, status_code=404, media_type="text/html")
    return HTMLResponse(
        "<h1>404 – Không tìm thấy trang</h1>"
        '<p>Liên hệ HTK: <a href="tel:0396241674">0396241674</a></p>',
        status_code=404,
    )


class VercelPathMiddleware:
    """Vercel rewrite '/(.*)' -> '/api/index/$1' đưa prefix /api/index vào path.

    Middleware ASGI khôi phục đường dẫn gốc để FastAPI định tuyến đúng
    (hoạt động cả local lẫn Vercel, không side-effect khi import).
    """

    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            prefix = "/api/index"
            if path == prefix or path.startswith(prefix + "/"):
                rest = path[len(prefix):] or "/"
                scope = dict(scope)
                scope["path"] = rest
                scope["raw_path"] = rest.encode("utf-8")
        await self.asgi_app(scope, receive, send)


app = VercelPathMiddleware(_fastapi)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)