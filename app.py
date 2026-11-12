from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="JPY-MMK & USD-MMK Rates Info Hub",
    page_icon="💸",
    layout="centered",
)


# Live Market Data & Myanmar Rates Info Fetching Function
@st.cache_data(ttl=60)
def get_market_data():
  try:
    # Global Exchange Rate API
    url_fx = "https://open.er-api.com/v6/latest/USD"
    res_fx = requests.get(url_fx, timeout=5).json()

    global_usd_jpy = 155.0
    global_usd_mmk = 2100.0
    if res_fx.get("result") == "success":
      rates = res_fx["rates"]
      global_usd_jpy = rates.get("JPY", 155.0)
      global_usd_mmk = rates.get("MMK", 2100.0)

    # RATES INFO (Myanmar Local / Open Market Simulation Rates)
    # ပြင်ပပေါက်ဈေး (Local Open Market Rates Reference)
    market_usd_buy = 4500.0  # ဥပမာ - ပြင်ပ USD ဝယ်ဈေး
    market_usd_sell = 4550.0  # ဥပမာ - ပြင်ပ USD ရောင်းဈေး
    market_jpy_rate = (
        market_usd_sell / global_usd_jpy
    )  # ပြင်ပပေါက်ဈေးအရ JPY နှုန်း

    # Gold Price API
    gold_oz = 2650.0
    try:
      url_gold = "https://data-asg.goldprice.org/dbjson/USD"
      res_gold = requests.get(url_gold, timeout=3).json()
      gold_oz = res_gold["items"][0]["xauPrice"]
    except Exception:
      pass

    return (
        market_jpy_rate,
        global_usd_jpy,
        market_usd_buy,
        market_usd_sell,
        gold_oz,
        "Live Market Connected",
    )
  except Exception:
    return 29.51, 155.0, 4500.0, 4550.0, 2650.0, "Offline Mode"


# Data Load
market_jpy, global_usdjpy, market_usdbuy, market_usdsell, gold_oz, source_status = (
    get_market_data()
)
current_time_str = datetime.now().strftime("%Y-ခုနှစ်၊ %m-လ၊ %d-ရက် (%H:%M နာရီ)")

# App Title & Header
st.markdown(
    "<h1 style='text-align: center;'>🇲🇲 🇯🇵 RATES INFO: Myanmar Market"
    " Hub</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align: center; color: gray;'>စနစ် အချိန်: {current_time_str}"
    " | Status: {source_status}</p>",
    unsafe_allow_html=True,
)

# ==================== 5 & 2nd Requirement: USD နှင့် JPY နှစ်ခုစလုံးအတွက် သတိပေးချက်များ ====================
st.warning(
    "⚠️ **လာမည့်တစ်ပတ်အတွက် အထူးသတိပေးချက် (Market Warning):**\n"
    "* **🇺🇸 ဒေါ်လာ (USD) ဈေးကွက်:** ပြင်ပပေါက်ဈေးနှင့် ဗဟိုဘဏ်မူဝါဒ"
    " အပြောင်းအလဲကြောင့် USD/MMK နှုန်းထားမှာ ပုံမှန်ထက် **သိသာစွာ အတက်/အကျ"
    " အစွန်းရောက်နိုင်ခြေ** ရှိပါသည်။\n* **🇯🇵 ဂျပန်ယန်း (JPY) ဈေးကွက်:**"
    " ကမ္ဘာ့ရွှေဈေးနှင့် USD/JPY တုန်ခါမှုများကြောင့် ယန်းဈေးနှုန်းများပါ"
    " မတည်ငြိမ်ဘဲ အတက်အကျကြမ်းနိုင်သဖြင့် အရောင်းအဝယ်ပြုလုပ်ရာတွင် အထူးဂရုပြုရန်"
    " သတိပေးအပ်ပါသည်။"
)

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💱 ပြင်ပပေါက်ဈေး & တွက်ချက်မှု",
    "📊 ဈေးနှုန်းဇယားများ",
    "🏛️ ဗဟိုဘဏ် သတင်းများ",
    "🥇 ကမ္ဘာ့ရွှေနှင့် ခန့်မှန်းချက်",
    "🎯 ခန့်မှန်းချက် မှန်ကန်မှု မှတ်တမ်း",
])

# ==================== TAB 1: 💱 ပြင်ပပေါက်ဈေး (RATES INFO) & တွက်ချက်မှု ====================
with tab1:
  st.subheader(
      "📌 RATES INFO: အမေရိကန်ဒေါ်လာနှင့် ဂျပန်ယန်း ပြင်ပပေါက်ဈေးများ"
  )

  # Display Cards for External Market Rates (RATES INFO Style)
  col_m1, col_m2, col_m3 = st.columns(3)
  col_m1.metric(
      label="💵 ပြင်ပ USD (ဝယ်ဈေး)", value=f"{market_usdbuy:,.0f} MMK"
  )
  col_m2.metric(
      label="💵 ပြင်ပ USD (ရောင်းဈေး)", value=f"{market_usdsell:,.0f} MMK"
  )
  col_m3.metric(
      label="💴 ပြင်ပ JPY (1 JPY နှုန်း)", value=f"{market_jpy:.2f} MMK"
  )

  st.divider()
  st.sidebar.header("⚙️ နှုန်းထား ချိန်ညှိရန်")
  spread = st.sidebar.slider(
      "Profit Margin / Spread (MMK)", 0.0, 5.0, 1.0, 0.1
  )

  buy_rate = market_jpy - spread
  sell_rate = market_jpy + spread

  st.subheader("🧮 ဂျပန်ယန်း ငွေလဲပမာဏ တွက်ချက်ရန်")
  jpy_amount = st.number_input(
      "ထည့်မည့် ဂျပန်ယန်း ပမာဏ (JPY)", min_value=1, value=10000, step=1000
  )
  calculated_mmk = jpy_amount * market_jpy
  st.success(
      f"💰 **{jpy_amount:,} JPY** = **{calculated_mmk:,.2f} MMK** (ပြင်ပပေါက်ဈေး"
      " အခြေခံဖြင့်)"
  )

  if st.button("🔄 နှုန်းထားအသစ် ရယူရန်"):
    st.rerun()

# ==================== TAB 2: 📊 Charts ====================
with tab2:
  st.subheader("📈 USD/MMK & JPY/MMK ပြင်ပပေါက်ဈေး Trend")
  dates = pd.date_range(end=datetime.now(), periods=7, freq="D")
  market_jpy_trend = [
      market_jpy - 0.4,
      market_jpy - 0.2,
      market_jpy + 0.1,
      market_jpy - 0.1,
    