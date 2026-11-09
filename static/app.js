// Bảng giá nông sản Bình Định 2026 – HTK · Hotline/Zalo: 0396241674
// Dữ liệu mô phỏng – cập nhật 09/11/2026
"use strict";

const fmt = (n) => new Intl.NumberFormat("vi-VN").format(n);

function changeHtml(pct) {
  if (pct > 0) return `<span class="change-up">▲ +${pct}%</span>`;
  if (pct < 0) return `<span class="change-down">▼ ${pct}%</span>`;
  return `<span class="change-flat">— 0%</span>`;
}

async function loadPrices() {
  const res = await fetch("/api/prices");
  const data = await res.json();
  const grid = document.getElementById("price-grid");
  const select = document.getElementById("product-select");
  const select2 = document.getElementById("district-product-select");
  grid.innerHTML = data.products
    .map(
      (p) => `
      <article class="card price-card">
        <h3>${p.name}</h3>
        <div class="price-value">${fmt(p.price)} <span class="price-unit">${p.unit}</span></div>
        <div>So với hôm qua: ${changeHtml(p.changePct)}</div>
        <p class="price-context">${p.context}</p>
      </article>`
    )
    .join("");
  for (const sel of [select, select2]) {
    sel.innerHTML = data.products
      .map((p) => `<option value="${p.id}">${p.name}</option>`)
      .join("");
  }
  await renderTrend(select.value);
  await renderDistricts(select2.value);
}

let trendChart = null;
let districtChart = null;

async function renderTrend(productId) {
  const res = await fetch(`/api/trend?product=${encodeURIComponent(productId)}`);
  const data = await res.json();
  document.getElementById("trend-title").textContent =
    `Xu hướng giá ${data.product} – 30 ngày (VNĐ/kg)`;
  if (trendChart) trendChart.destroy();
  trendChart = new Chart(document.getElementById("trend-chart"), {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: `${data.product} (VNĐ/kg)`,
          data: data.prices,
          borderColor: "#1b7a3d",
          backgroundColor: "rgba(27,122,61,.12)",
          fill: true,
          tension: 0.3,
          pointRadius: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } },
      scales: { y: { ticks: { callback: (v) => fmt(v) } } },
    },
  });
}

async function renderDistricts(productId) {
  const res = await fetch(`/api/by-district?product=${encodeURIComponent(productId)}`);
  const data = await res.json();
  document.getElementById("district-title").textContent =
    `So sánh giá ${data.product} theo 11 huyện/thị/thành Bình Định (VNĐ/kg)`;
  const tbody = document.getElementById("district-tbody");
  tbody.innerHTML = data.districts
    .map(
      (d) => `<tr><td>${d.district}</td><td>${fmt(d.price)}</td><td>${changeHtml(d.diffPct)}</td></tr>`
    )
    .join("");
  if (districtChart) districtChart.destroy();
  districtChart = new Chart(document.getElementById("district-chart"), {
    type: "bar",
    data: {
      labels: data.districts.map((d) => d.district),
      datasets: [
        {
          label: `${data.product} (VNĐ/kg)`,
          data: data.districts.map((d) => d.price),
          backgroundColor: "rgba(27,122,61,.75)",
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { ticks: { callback: (v) => fmt(v) } } },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("price-grid")) return;
  loadPrices().catch((err) => {
    document.getElementById("price-grid").innerHTML =
      '<p class="card">Không tải được dữ liệu. Vui lòng thử lại hoặc gọi HTK: <a href="tel:0396241674">0396241674</a>.</p>';
    console.error(err);
  });
  document.getElementById("product-select").addEventListener("change", (e) => {
    renderTrend(e.target.value);
    document.getElementById("district-product-select").value = e.target.value;
    renderDistricts(e.target.value);
  });
  document.getElementById("district-product-select").addEventListener("change", (e) => {
    renderDistricts(e.target.value);
  });
});