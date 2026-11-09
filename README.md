# 🌾 binhdinh-agri-price — Bảng giá nông sản Bình Định 2026

**Stack:** Python FastAPI · **Deploy:** Vercel · **Cập nhật: 09/11/2026**

## Vấn đề

Cuối năm 2026, nông dân Bình Định không nắm được giá lúa, sắn (mì), tiêu, điều và các
nông sản chủ lực nên thường bị thương lái ép giá. **Mùa mưa lũ 2026** — lũ sông Kôn dâng
cao ở Tuy Phước, An Nhơn; bão số 9, số 10 đổ bộ Quy Nhơn – Phù Cát – Hoài Nhơn; sạt lở
An Lão, Vĩnh Thạnh, Tây Sơn; mất điện diện rộng 3–7 ngày — làm chuỗi thu mua gián đoạn,
chênh lệch giá giữa 11 huyện ngày càng lớn. Trang này giúp bà con theo dõi giá tham khảo,
xu hướng 30 ngày và chọn nơi bán có lợi nhất.

> ⚠️ **Dữ liệu mô phỏng – cập nhật 09/11/2026** — không phải giá thu mua chính thức.

## Tính năng

- **Bảng giá 10 loại nông sản** (VNĐ/kg): lúa, sắn (mì), tiêu, điều, bắp, đậu phộng, mè, khoai lang, mía, đậu xanh — giá hiện tại + thay đổi % so với hôm qua.
- **Biểu đồ Chart.js xu hướng giá 30 ngày**, chọn loại nông sản.
- **So sánh giá theo 11 huyện Bình Định**: Quy Nhơn, An Nhơn, Tuy Phước, Phù Cát, Phù Mỹ, Hoài Nhơn, Hoài Ân, Vĩnh Thạnh, Tây Sơn, An Lão, Vân Canh (biểu đồ cột + bảng).
- Trang chủ mô tả vấn đề, trang Giới thiệu, trang 404 có hotline HTK.
- Responsive 375px – 1440px, UI tiếng Việt.

## API (FastAPI)

| Endpoint | Mô tả |
|---|---|
| `GET /api/prices` | Giá hiện tại 10 loại + thay đổi % |
| `GET /api/trend?product=lua` | Chuỗi giá 30 ngày của 1 loại |
| `GET /api/by-district?product=tieu` | Giá theo 11 huyện của 1 loại |

`product` ∈ `lua, san, tieu, dieu, bap, dau-phong, me, khoai-lang, mia, dau-xanh`.

## Công nghệ

- Backend: **Python FastAPI** + Uvicorn (ASGI chạy trực tiếp trên Vercel, middleware khôi phục path sau rewrite).
- Frontend: HTML/CSS/JS thuần + Chart.js (CDN), fetch API.
- Deploy: Vercel (`vercel.json` rewrite `/(.*) → /api/index/$1`).

## Cách chạy local

```bash
py -m venv venv
venv/Scripts/python.exe -m pip install -r requirements.txt
venv/Scripts/python.exe api/index.py
# Mở http://127.0.0.1:8000
```

## Deploy

- Vercel: **https://binhdinh-agri-price.vercel.app** (xem `deploy_url.txt`)
- GitHub: https://github.com/shirmtry/binhdinh-agri-price

## 📞 Liên hệ HTK – 0396241674 – 09/11/2026

- Tác giả: **HTK**
- Hotline/Zalo: **0396241674** — [tel:0396241674](tel:0396241674) · https://zalo.me/0396241674
- Email: htk.contact@gmail.com
- Cập nhật: **09/11/2026** (mùa mưa lũ 2026 Bình Định)

© 2026 HTK · Hotline/Zalo: 0396241674 · Email: htk.contact@gmail.com