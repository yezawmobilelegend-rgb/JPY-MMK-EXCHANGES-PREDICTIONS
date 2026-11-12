import streamlit as st
import pandas as pd

st.title("🇯🇵 🇲🇲 JPY-MMK Smart Exchange Dashboard")
st.sidebar.header("ဈေးကွက် အချက်အလက် ထည့်သွင်းရန်")

# 1. Input Data
domestic_usd = st.sidebar.number_input("ပြည်တွင်း USD ပြင်ပပေါက်ဈေး (MMK)", value=4500.0, step=50.0)
intl_usdjpy = st.sidebar.number_input("နိုင်ငံတကာ USD/JPY ဈေး (TradingView/Forex.com)", value=152.50, step=0.1)
business_spread = st.sidebar.slider("လုပ်ငန်းသုံး အမြတ် Spread (MMK)", min_value=1.0, max_value=10.0, value=3.0)

# 2. Calculation (Formula)
base_jpy_rate = domestic_usd / intl_usdjpy
my_buy_rate = base_jpy_rate - business_spread
my_sell_rate = base_jpy_rate + business_spread

st.subheader("📊 တွက်ချက်ပြီးသော ယန်းပေါက်ဈေးနှုန်းများ")
col1, col2, col3 = st.columns(3)
col1.metric("အခြေခံ ယန်းပေါက်ဈေး", f"{base_jpy_rate:.2f} MMK")
col2.metric("သင့်ရဲ့ ဝယ်ဈေး (Buy Rate)", f"{my_buy_rate:.2f} MMK")
col3.metric("သင့်ရဲ့ အရောင်းဈေး (Sell Rate)", f"{my_sell_rate:.2f} MMK")

st.divider()

st.subheader("အကြံပြုချက်နှင့် ဈေးကွက်လမ်းညွှန်")
if intl_usdjpy > 153.0:
  st.warning(
      "⚠️ နိုင်ငံတကာတွင် ယန်းတန်ဖိုး အားနည်းနေပါသည်။ ယန်းအများအပြား"
      " ဝင်ဝယ်စုဆောင်းရန် ဂရုစိုက်ပါ။ ဈေးကွက်ကို စောင့်ကြည့်ပါ[span_15](start_span)[span_15](end_span)."
  )
else:
  st.success(
      "✅ ယန်းဈေး တည်ငြိမ်နေပါသည်။ သတ်မှတ်ထားသော Spread ဖြင့်"
      " ပုံမှန်အရောင်းအဝယ် လုပ်ဆောင်နိုင်ပါသည်။"
  )

st.info(
    "💡 အကြံပြုချက် - Forex.com ရှိ Economic Calendar တွင် Fed နှင့် BOJ"
    " သတင်းများ ထွက်မည့်အချိန်များတွင် ဈေးနှုန်းကို ခတ္တဆိုင်းငံ့ထားပါ။"
)
