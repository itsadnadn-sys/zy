import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="个人信息管理系统（练习版）", page_icon="🌱", layout="wide")

BASE_DIR = Path().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "records.csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)


COLUMNS = ["id", "title", "category", "notes", "created_at","start_date", "priority","tags"]
df = pd.read_csv(CSV_PATH, usecols=COLUMNS)


def load_data() -> pd.DataFrame:
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH,dtype={"id":int})
        for col in COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        df = pd.DataFrame(columns=COLUMNS)
    return df


def save_data(df: pd.DataFrame):
    try:
        df.to_csv(CSV_PATH, index=False, encoding="utf-8")
        pass
    except Exception:
        pass


def input_form(df: pd.DataFrame) -> pd.DataFrame:
    with st.form("add_form", clear_on_submit=True):
        new = {}
        new["id"] = (0 if df.empty else int(df["id"].max()) + 1)

        new["title"] = st.text_input("标题 *", placeholder="例如：三好学生")
        CATEGORIES = ["荣誉", "教育经历", "竞赛", "证书", "账号", "其他"]
        new["category"] = st.selectbox("类别", CATEGORIES, index=0)
        new["notes"] = st.text_area("备注（可选）", placeholder="关键信息、链接或行动项…", height=100)

        submitted = st.form_submit_button("保存", type="primary", use_container_width=True)

        new["started_date"] = st.date_input("开始日期", value=pd.Timestamp.now())
        new["priority"] = st.slider("优先级", min_value=1, max_value=5, value=3, help="0=低优先级，3=高优先级")
        TAGS = ["重要", "紧急", "待跟进", "个人"]
        selected_tags = st.multiselect("标签（可多选）", TAGS, default=[])
        new["tags"] = ",".join(selected_tags)
        submitted = st.form_submit_button("保存", type="primary", use_container_width=True)

    if submitted:
        new["created_at"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

        new["start_date"] = new["start_date"].strftime("%Y-%m-%d")

        df_new = pd.DataFrame(new, index=[0])
        df = pd.concat([df, df_new], ignore_index=True)
        save_data(df)
        st.success("已保存 ✅")


    return df


df = load_data()

st.title("🌱个人信息管理系统")
st.caption("用于记录荣誉、教育经历、竞赛等个人重要信息，支持数据保存与导出")

st.subheader("已保存记录",divider='gray')

st.dataframe(df,use_container_width=True,hide_index=True)
if not df.empty:
    csv_data = df.to_csv(index=False, encoding="utf-8")
    st.download_button(label="下载全部记录(CSV)",data=csv_data,file_name="personal_records.csv",
                       mime="text/csv",use_container_width=True)
else:
    st.info("暂无记录，请添加第一条记录吧！")


st.write("🌱 个人MIS（入门单文件） — 请在 Todo5 补齐页面标题、说明与输出。")


df = input_form(df)

st.write("当前数据（简化输出）：")
st.write(df)