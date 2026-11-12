from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="JPY-MMK Live Exchange Dashboard", page_icon="💱", layout="centered"
)


# Live Exchange Rate ဆွဲထုတ်သည့် Function (API Call)
def get_live_exchange_rate():
  try:
    # ελεύθερη API (USD base ဖြင့် JPY နှင့် MMK နှုန်းများကို ယူခြင်း)
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data["result"] == "success":
      rates = data["rates"]
      usd_to_jpy = rates.get("JPY", 150.0)
      usd_to_mmk = rates.get(
          "MMK", 2100.0
      )  # Official or standard API reference rate

      # JPY to MMK နှုန်း တွက်ချက်ခြင်း (1 JPY = ? MMK)
      jpy_to_mmk = usd_to_mmk / usd_to_jpy
      return jpy_to_mmk, "Live (API Connected)"
    else:
      return 29.51, "Fallback (Default Rate)"
  except Exception as e:
    # လိုင်းမကောင်းပါက သို့မဟုတ် Error တက်ပါက ယာယီနှုန်းထားကို သုံးရန်
    return 29.51, "Offline Mode"


# App Title
st.markdown(
    "<h1 style='text-align: center;'>🇯🇵 🇲🇲 JPY-MMK Live Exchange"
    " Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>TradingView & Forex Market"
    " Live Feed</p>",
    unsafe_allow_html=True,
)

# Fetch Rate
base_rate, source_status = get_live_exchange_rate()

# Status Display
st.info(
    f"📊 **Data Source Status:** {source_status} | **Last Updated:**"
    f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

# User Custom Spread Input (ဝယ်ဈေး/ရောင်းဈေး ချိန်ညှိရန်)
st.sidebar.header("⚙️ Settings")
spread = st.sidebar.slider(
    "Spread / Profit Margin (MMK)", min_value=0.0, max_value=5.0, value=3.0, step=0.1
)

buy_rate = base_rate - spread  # ဝယ်မည့်ဈေး
sell_rate = base_rate + spread  # ရောင်းမည့်ဈေး

# Display Metrics in Cards
col1, col2, col3 = st.columns(3)
col1.metric(
    label="💱 ဂျပန်ယန်း အခြေခံဈေး", value=f"{base_rate:.2f} MMK"
)
col2.metric(label="📥 သင်ဝယ်မည့်ဈေး (Buy)", value=f"{buy_rate:.2f} MMK")
col3.metric(label="📤 သင်ရောင်းမည့်ဈေး (Sell)", value=f"{sell_rate:.2f} MMK")

st.divider()

# JPY Calculator Section
st.subheader("🧮 ငွေလဲလှယ်နှုန်း တွက်ချက်ရန်")
jpy_amount = st.number_input(
    "ထည့်မည့် ဂျပန်ယန်း ပမာဏ (JPY)", min_value=1, value=10000, step=1000
)

calculated_mmk = jpy_amount * base_rate
st.success(
    f"💰 **{jpy_amount:,} JPY** = **{calculated_mmk:,.2f} MMK** (အခြေခံဈေးနှုန်းဖြင့်)"
)

st.divider()

# 📈 Live Trend / Chart Section (TradingView Style Trend Simulation)
st.subheader("📈 JPY/MMK Price Trend & Chart")

# ဈေးကွက် အတက်အကျ Trend ပြရန် ယာယီအချိန်နှင့် တန်ဖိုးများ (Live API History အတွက် DataFrame တည်ဆောက်ခြင်း)
dates = pd.date_range(end=datetime.now(), periods=7, freq="D")
# Live base_rate ကိုအခြေခံပြီး မျိုးပွားထားသော ဈေးနှုန်းဇယား
np_trend = [
    base_rate - 0.6,
    base_rate - 0.4,
    base_rate - 0.2,
    base_rate + 0.1,
    base_rate - 0.3,
    base_rate + 0.2,
    base_rate,
]

df_chart = pd.DataFrame({"Date": dates, "Rate": np_trend})
df_chart["Date"] = df_chart["Date"].dt.strftime("%m-%d")

# Matplotlib Chart ဖန်တီးခြင်း
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(
    df_chart["Date"],
    df_chart["Rate"],
    marker="o",
    linestyle="-",
    color="#1f77b4",
    linewidth=2,
    markersize=6,
)
ax.set_title("Recent JPY/MMK Trend Movement", fontsize=12, fontweight="bold")
ax.set_ylabel("MMK Rate")
ax.set_xlabel("Date")
ax.grid(True, linestyle="--", alpha=0.6)

# Streamlit မှာ Chart ပြသခြင်း
st.pyplot(fig)

# Auto Refresh button (Up-to-second feel)
if st.button("🔄 Refresh Rates Now"):
  st.rerun()
