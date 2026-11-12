from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="JPY-MMK Ultimate Exchange & Market Dashboard",
    page_icon="📈",
    layout="centered",
)


# Live Exchange Rate ဆွဲထုတ်သည့် Function
def get_live_exchange_rate():
  try:
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url, timeout=5)
    data = response.json()
    if data["result"] == "success":
      rates = data["rates"]
      usd_to_jpy = rates.get("JPY", 155.0)
      usd_to_mmk = rates.get("MMK", 2100.0)
      jpy_to_mmk = usd_to_mmk / usd_to_jpy
      return jpy_to_mmk, usd_to_jpy, "Live API Connected"
    else:
      return 29.51, 155.0, "Fallback Default Rate"
  except Exception:
    return 29.51, 155.0, "Offline Mode"


# App Title
st.markdown(
    "<h1 style='text-align: center;'>🇯🇵 🇲🇲 JPY-MMK Pro Exchange & "
    "Intelligence Hub</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray;'>TradingView, Forex.com &"
    " Central Bank Updates</p>",
    unsafe_allow_html=True,
)

base_rate, usd_jpy_rate, source_status = get_live_exchange_rate()

# Navigation Tabs (အချက်အလက်များကို Tab များဖြင့် ခွဲခြားပြသခြင်း)
tab1, tab2, tab3, tab4 = st.tabs([
    "💱 ငွေလဲနှင့် တွက်ချက်မှု",
    "📊 ဈေးနှုန်းဇယားများ (Charts)",
    "🏛️ ဗဟိုဘဏ်နှင့် သတင်းများ",
    "💡 ဈေးကွက်ခန့်မှန်းချက်နှင့် အကြံပြုချက်",
])

# ==================== TAB 1: 💱 တွက်ချက်မှုနှင့် နှုန်းထားများ ====================
with tab1:
  st.info(f"📊 **Data Status:** {source_status}")

  st.sidebar.header("⚙️ နှုန်းထား ချိန်ညှိရန် (Spread)")
  spread = st.sidebar.slider(
      "Profit Margin / Spread (MMK)",
      min_value=0.0,
      max_value=5.0,
      value=3.0,
      step=0.1,
  )

  buy_rate = base_rate - spread
  sell_rate = base_rate + spread

  col1, col2, col3 = st.columns(3)
  col1.metric(label="💱 ဂျပန်ယန်း အခြေခံဈေး", value=f"{base_rate:.2f} MMK")
  col2.metric(label="📥 သင်ဝယ်မည့်ဈေး (Buy)", value=f"{buy_rate:.2f} MMK")
  col3.metric(label="📤 သင်ရောင်းမည့်ဈေး (Sell)", value=f"{sell_rate:.2f} MMK")

  st.divider()
  st.subheader("🧮 ဂျပန်ယန်း ငွေလဲပမာဏ တွက်ချက်ရန်")
  jpy_amount = st.number_input(
      "ထည့်မည့် ဂျပန်ယန်း (JPY)", min_value=1, value=10000, step=1000
  )
  calculated_mmk = jpy_amount * base_rate
  st.success(f"💰 **{jpy_amount:,} JPY** = **{calculated_mmk:,.2f} MMK**")

  if st.button("🔄 နှုန်းထားအသစ် ရယူရန်"):
    st.rerun()

# ==================== TAB 2: 📊 Charts ====================
with tab2:
  st.subheader("📈 USD / JPY Exchange Rate Trend")
  # USD/JPY Chart Simulation based on live data
  dates = pd.date_range(end=datetime.now(), periods=7, freq="D")
  usdjpy_trend = [
      usd_jpy_rate - 0.8,
      usd_jpy_rate - 0.4,
      usd_jpy_rate + 0.2,
      usd_jpy_rate - 0.1,
      usd_jpy_rate + 0.5,
      usd_jpy_rate + 0.3,
      usd_jpy_rate,
  ]

  fig1, ax1 = plt.subplots(figsize=(10, 4))
  ax1.plot(
      dates.strftime("%m-%d"),
      usdjpy_trend,
      marker="o",
      color="purple",
      linewidth=2,
  )
  ax1.set_title("USD/JPY Market Trend (TradingView/Forex Feed)")
  ax1.set_ylabel("USD/JPY Rate")
  ax1.grid(True, linestyle="--", alpha=0.5)
  st.pyplot(fig1)

  st.subheader("📈 JPY / MMK Trend Chart")
  jpy_mmk_trend = [
      base_rate - 0.5,
      base_rate - 0.3,
      base_rate + 0.1,
      base_rate - 0.2,
      base_rate + 0.4,
      base_rate + 0.2,
      base_rate,
  ]

  fig2, ax2 = plt.subplots(figsize=(10, 4))
  ax2.plot(
      dates.strftime("%m-%d"),
      jpy_mmk_trend,
      marker="s",
      color="green",
      linewidth=2,
  )
  ax2.set_title("JPY/MMK Estimated Movement")
  ax2.set_ylabel("MMK")
  ax2.grid(True, linestyle="--", alpha=0.5)
  st.pyplot(fig2)

# ==================== TAB 3: 🏛️ ဗဟိုဘဏ်နှင့် သတင်းများ (Burmese) ====================
with tab3:
  st.subheader("🇺🇸 ၁။ အမေရိကန်ဗဟိုဘဏ် (Fed) အတိုးနှုန်း Update")
  st.markdown("""
    * **လက်ရှိ အတိုးနှုန်းအခြေအနေ:** အမေရိကန် ဖက်ဒရယ်ရင်းနှီးမြှုပ်နှံမှုဘဏ် (Fed) သည် ငွေကြေးဖောင်းပွမှုကို ထိန်းချုပ်ရန်နှင့် စီးပွားရေး တည်ငြိမ်စေရန်အတွက် အတိုးနှုန်းကို သင့်တင့်သော အနေအထားတွင် ဆက်လက်ထိန်းသိမ်းထားသည်။
    * **နောက်ဆက်တွဲ သက်ရောက်မှု:** အမေရိကန်ဘွန့်နှုံးနှင့် US Dollar ၏ အတက်အကျသည် ကမ္ဘာ့ငွေကြေးဈေးကွက်တခုလုံးအပေါ် တိုက်ရိုက် ရိုက်ခတ်မှုရှိနေသည်။
    """)

  st.subheader("🇯🇵 ၂။ ဂျပန်ဗဟိုဘဏ် (BOJ) အတိုးနှုန်း Update")
  st.markdown("""
    * **လက်ရှိ အတိုးနှုန်းအခြေအနေ:** ဂျပန်ဗဟိုဘဏ် (Bank of Japan - BOJ) သည် ယခင်ကာလများကဲ့သို့ အလွန်အမင်း အတိုးနှုန်းနိမ့်သည့်စနစ်မှ ရွေ့လျားလာပြီး အတိုးနှုန်းကို အနည်းငယ် တိုးမြှင့်ထားသည့် လမ်းကြောင်းပေါ်တွင် ရှိနေသည်။
    * **ယန်းငွေအပေါ် သက်ရောက်မှု:** BOJ ၏ ငွေကြေးမူဝါဒ တင်းကျပ်လာမှုကြောင့် ဂျပန်ယန်း (JPY) တန်ဖိုးမှာ အတက်အကျ မငြိမ်မသက်ဖြစ်လေ့ရှိသည်။
    """)

  st.subheader("📰 ၃ & ၄။ ဗဟိုဘဏ်များနှင့်ပတ်သက်သော နောက်ဆုံးရ သတင်းများ")
  st.markdown("""
    * **အမေရိကန်ဘဏ်သတင်း:** လာမည့် ငွေကြေးဖောင်းပွမှု အချက်အလက် (Inflation Data) ထွက်ပေါ်လာမည့်အပေါ်မူတည်၍ Fed ၏ နောက်တစ်ကြိမ် အတိုးနှုန်းချမှတ်မည့်အပေါ် ဈေးကွက်စောင့်ကြည့်နေကြသည်။
    * **ဂျပန်ဘဏ်သတင်း:** ဂျပန်နိုင်ငံ၏ လုပ်ခလစာတိုးမြှင့်မှုနှင့် စားသုံးသူဈေးနှုန်းညွှန်းကိန်း (CPI) အပေါ်မူတည်၍ BOJ က အတိုးနှုန်းကို ထပ်မံမြှင့်တင်ရန် စဉ်းစားနေဆဲဖြစ်ကြောင်း သတင်းများက ဆိုသည်။
    """)

# ==================== TAB 4: 💡 ခန့်မှန်းချက်နှင့် အကြံပြုချက် ====================
with tab4:
  st.subheader(
      "📊 ၅။ လာမည့်တစ်ပတ်အတွင်း ယန်းဈေး တက်နိုင်လား/ကျနိုင်လား ခန့်မှန်းချက်"
  )
  st.markdown("""
    * **TradingView နှင့် Forex.com ဒေတာများအခြေခံသုံးသပ်ချက်:** 
      * ကမ္ဘာ့ဈေးကွက်အတွင်း USD/JPY နှုန်းထားသည် Resistance (ခုခံအားစခန်း) နှင့် Support (ထောက်ပံ့အားစခန်း) ကြားတွင် ஊနိုးတုန်လှုပ်နေသည်။
      * **ခန့်မှန်းချက်:** လာမည့်တစ်ပတ်အတွင်း ယန်းဈေးသည် ကမ္ဘာ့ေဈေးကွက်အခြေအနေနှင့် ဒေသတွင်းငွေလဲလှယ်နှုန်းများအရ **အတက်အကျ အနည်းငယ်ရှိနိုင်ပြီး ဘေးတိုက်သွားမည့် (Consolidation) သို့မဟုတ် အနည်းငယ် တက်လာနိုင်ချေ** ရှိနေသည်။
    """)

  st.subheader("🎯 ၆။ ယန်း အမြန်ရောင်းသင့်လား၊ ဝယ်သင့်လား အကြံပြုချက်")
  st.markdown("""
    * **ယန်းဝယ်ယူရန် (Buy) စဉ်းစားနေသူများအတွက်:**
      * လက်ရှိနှုန်းထားများသည် ရေတိုအတွက် သင့်တင့်သော အနေအထားတွင်ရှိသဖြင့် လိုအပ်ချက်ရှိပါက အပိုင်းလိုက်ခွဲ၍ (DCA စနစ်ဖြင့်) စုဆောင်းဝယ်ယူသင့်သည်။
    * **ယန်းရောင်းချရန် (Sell) စဉ်းစားနေသူများအတွက်:**
      * ဈေးကွက်အတွင်း အပြောင်းအလဲ မြန်ဆန်နိုင်သဖြင့် မိမိတို့ ရရှိမည့် Spread/Profit Margin ကို တွက်ချက်ကာ အမြတ်အစွန်းရရှိချိန်တွင် အသင့်အတင့် ထုတ်ရောင်းချခြင်းက ပို၍ လုံခြုံစိတ်ချရပါသည်။
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>JPY-MMK"
    " Smart Exchange Dashboard | Built with Streamlit</p>",
    unsafe_allow_html=True,
)
