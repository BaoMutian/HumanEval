import streamlit as st
import json
import os
import html
import pandas as pd
from judge_prompt import CHECKLISTS

# Configuration
DATA_FILE = "100_llama3.1-70b-instruct_human_eval_gpt-4o.jsonl"
FULL_DATASET_FILE = "geoqa_reason/full_dataset.jsonl"
OUTPUT_DIR = "human_eval_results"  # Directory to store results

st.set_page_config(layout="wide", page_title="GeoQA Human Evaluation")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load full dataset questions


@st.cache_data
def load_full_dataset_questions():
    """Load questions from full dataset indexed by task_name and numeric id"""
    questions_map = {}
    if os.path.exists(FULL_DATASET_FILE):
        with open(FULL_DATASET_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    # Extract numeric part from id like "2_336" -> "336"
                    full_id = record.get('id', '')
                    task_name = record.get('task_name', '')
                    question = record.get('question', '')

                    if '_' in full_id:
                        numeric_id = full_id.split('_')[-1]
                        key = f"{task_name}_{numeric_id}"
                        questions_map[key] = question
    return questions_map


questions_map = load_full_dataset_questions()

# Load Data


@st.cache_data
def load_data():
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    # Match question from full dataset
                    task_name = record.get('task_name', '')
                    record_id = record.get('id', '')
                    key = f"{task_name}_{record_id}"
                    record['question'] = questions_map.get(
                        key, 'Question not found in full dataset')
                    data.append(record)
    return data


data = load_data()

# Initialize annotator name in session state
if 'annotator_name' not in st.session_state:
    st.session_state.annotator_name = ""

# Function to get output file for annotator


def get_output_file(annotator_name):
    if not annotator_name:
        return None
    # Clean filename
    safe_name = "".join(c for c in annotator_name if c.isalnum()
                        or c in (' ', '_', '-')).strip()
    safe_name = safe_name.replace(' ', '_')
    return os.path.join(OUTPUT_DIR, f"human_eval_results_{safe_name}.jsonl")

# Function to load processed IDs for current annotator


def load_processed_ids(annotator_name):
    processed_ids = set()
    output_file = get_output_file(annotator_name)
    if output_file and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        rec = json.loads(line)
                        processed_ids.add(rec.get("id"))
                    except:
                        pass
    return processed_ids


# Load processed IDs for current user
processed_ids = load_processed_ids(st.session_state.annotator_name)

# Initialize Session State
if 'current_index' not in st.session_state:
    # Try to find the first unprocessed index
    first_unprocessed = 0
    for i, d in enumerate(data):
        if d.get('id') not in processed_ids:
            first_unprocessed = i
            break
    st.session_state.current_index = first_unprocessed

# Helper to save result


def save_result(record, human_reason_score, human_answer_score, human_comment, task_type, annotator_name):
    output_file = get_output_file(annotator_name)
    if not output_file:
        st.error("请先输入标注者姓名！")
        return False

    result_entry = {
        "id": record.get("id"),
        "annotator_name": annotator_name,
        "human_reason_score": human_reason_score,
        "human_answer_score": human_answer_score,
        "human_total_score": human_reason_score + human_answer_score,
        "human_comment": human_comment,
        "task_type": task_type,
        "original_record": record
    }

    # Append to file
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result_entry, ensure_ascii=False) + "\n")

    # Update processed set
    processed_ids.add(record.get("id"))
    st.success(f"✅ 已保存记录 ID {record.get('id')} (标注者: {annotator_name})")

    # Auto-advance to next unprocessed
    if st.session_state.current_index < len(data) - 1:
        st.session_state.current_index += 1
        st.rerun()

    return True

# Helper to detect task type


def detect_task_type(record):
    gt = record.get('ground_truth', '')
    resp = record.get('response', '')

    if 'Bearing:' in gt and 'Cardinal direction:' in gt:
        return 'direction'
    if '->' in gt:
        return 'planning'
    if any(x in gt for x in ['Intersecting', 'Parallel', 'Disconnected']):
        return 'relation-r2r'
    if any(x in gt for x in ['Pass through', 'Touch the area', 'Lie outside']):
        return 'relation-r2a'
    if any(x in gt for x in ['Overlapping', 'Adjacent', 'Separate']):
        return 'relation-a2a'
    # Heuristics for others
    if 'km' in gt or 'miles' in gt or 'meters' in gt:
        # Simple check, might be weak
        return 'distance'

    return 'distance'  # Default


# Sidebar
st.sidebar.title("标注系统")

# Annotator name input
st.sidebar.subheader("👤 标注者信息")
annotator_input = st.sidebar.text_input(
    "请输入您的姓名",
    value=st.session_state.annotator_name,
    placeholder="例如: 张三",
    help="每位标注者的结果将保存到独立的文件中"
)

# Update annotator name and reload if changed
if annotator_input != st.session_state.annotator_name:
    st.session_state.annotator_name = annotator_input
    # Reload processed IDs for new annotator
    processed_ids = load_processed_ids(annotator_input)
    # Find first unprocessed for this annotator
    first_unprocessed = 0
    for i, d in enumerate(data):
        if d.get('id') not in processed_ids:
            first_unprocessed = i
            break
    st.session_state.current_index = first_unprocessed
    st.rerun()

# Display annotator file info
if st.session_state.annotator_name:
    output_file = get_output_file(st.session_state.annotator_name)
    st.sidebar.success(f"✓ 当前标注者: **{st.session_state.annotator_name}**")
    st.sidebar.caption(f"保存文件: `{os.path.basename(output_file)}`")
else:
    st.sidebar.warning("⚠️ 请先输入姓名才能开始标注")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 标注进度")
total_records = len(data)
processed_count = len(processed_ids)
st.sidebar.write(f"已完成: {processed_count} / {total_records}")
st.sidebar.progress(
    processed_count / total_records if total_records > 0 else 0)

# Navigation buttons
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 导航")
col_prev, col_next = st.sidebar.columns(2)
if col_prev.button("⬅️ 上一条"):
    st.session_state.current_index = max(0, st.session_state.current_index - 1)
if col_next.button("下一条 ➡️"):
    st.session_state.current_index = min(
        total_records - 1, st.session_state.current_index + 1)

# Jump to index
selected_index = st.sidebar.number_input(
    "跳转到索引", min_value=0, max_value=total_records-1, value=st.session_state.current_index)
st.session_state.current_index = selected_index

# Statistics
if processed_count > 1 and st.session_state.annotator_name:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 实时统计")
    try:
        output_file = get_output_file(st.session_state.annotator_name)
        results = []
        if output_file and os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        results.append(json.loads(line))
        if results:
            df = pd.DataFrame(results)
            df['llm_total_score'] = df['original_record'].apply(lambda x: float(
                x.get('total_score', 0)) if x.get('total_score') is not None else 0.0)

            # Display average scores
            avg_human = df['human_total_score'].mean()
            avg_llm = df['llm_total_score'].mean()
            st.sidebar.metric("平均人工评分", f"{avg_human:.2f}")
            st.sidebar.metric("平均LLM评分", f"{avg_llm:.2f}")

            if len(df) > 1:
                corr = df['human_total_score'].corr(df['llm_total_score'])
                st.sidebar.metric("相关系数", f"{corr:.4f}")
    except Exception as e:
        st.sidebar.error(f"统计错误: {e}")

# Main Content
if data:
    record = data[st.session_state.current_index]

    st.title(
        f"记录 {st.session_state.current_index + 1} / {total_records} (ID: {record.get('id')})")

    if record.get('id') in processed_ids:
        st.info("✓ 您已经标注过此记录")

    # Task Type Selection
    detected_type = detect_task_type(record)
    task_type = st.selectbox("任务类型 (Task Type)", list(CHECKLISTS.keys()), index=list(
        CHECKLISTS.keys()).index(detected_type) if detected_type in CHECKLISTS else 0)

    # Display Content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("数据内容")
        st.markdown("**问题 (Question):**")
        question_text = record.get('question', 'N/A')
        if question_text == 'Question not found in full dataset':
            st.warning(question_text)
        else:
            st.info(question_text)

        st.markdown("**标准答案 (Ground Truth):**")
        st.success(record.get('ground_truth', 'N/A'))

        st.markdown("**模型回答 (Model Response):**")
        st.text_area("Response", record.get('response', ''), height=800)

    with col2:
        st.subheader("评分区")

        # Display Rubric
        with st.expander("评分标准 (Checklist)", expanded=True):
            rubric_text = CHECKLISTS.get(task_type, "未找到此任务类型的评分标准。")
            escaped_text = html.escape(rubric_text)
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 8px; 
                    border: 1px solid #e9ecef;
                    font-family: 'Source Sans Pro', sans-serif;
                    font-size: 14px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                    color: #212529;
                ">{escaped_text}</div>
                """,
                unsafe_allow_html=True
            )

        # Scoring Form
        if not st.session_state.annotator_name:
            st.warning("⚠️ 请先在左侧输入您的姓名才能开始标注")

        # Determine max reason score based on task type
        reason_max_score = 15 if task_type in [
            'distance', 'direction', 'relation-r2r', 'relation-r2a', 'relation-a2a'] else 20

        with st.form(key=f"score_form_{record.get('id')}"):
            # Put both scores in one row
            score_col1, score_col2 = st.columns(2)
            with score_col1:
                h_reason = st.number_input(
                    f"推理得分 (0-{reason_max_score})",
                    min_value=0,
                    max_value=reason_max_score,
                    step=1,
                    value=0
                )
            with score_col2:
                h_answer = st.number_input(
                    "答案得分 (0-10)",
                    min_value=0,
                    max_value=10,
                    step=1,
                    value=0
                )

            total_human = h_reason + h_answer
            st.markdown(
                f"**总分 (Total Score):** {total_human} / {reason_max_score + 10}")

            submit_button = st.form_submit_button(
                label="💾 保存评分", disabled=not st.session_state.annotator_name)

            if submit_button:
                if st.session_state.annotator_name:
                    save_result(record, h_reason, h_answer, "",
                                task_type, st.session_state.annotator_name)
                else:
                    st.error("请先输入标注者姓名！")

else:
    st.write("未找到数据。")
