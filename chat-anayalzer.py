import streamlit as st
import time
import string
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Chat Analyzer", layout="wide")

st.title("🪄 CHAT-ANALYZER")
st.subheader("⚜️ Upload Your Files and We Do the MAGIC for You")

uploaded_file = st.file_uploader("🧛 Upload your file here (txt only)", type="txt")
placeholder = st.empty()

if uploaded_file is not None:
    placeholder.markdown("""
        <style>
        .blink { animation: blinker 1s linear infinite; color: white; font-weight: bold; font-size: 22px; }
        @keyframes blinker { 50% { opacity: 0; } }
        </style>
        <div class="blink">Processing your chat...</div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()
    st.success("Upload completed ✅")

    # ===== Read lines =====
    lines = uploaded_file.read().decode("utf-8").splitlines()
    usr, sys = [], []
    s = u = 0

    for line in lines:
        line = line.rstrip("\n")
        if '-' in line:
            parts = line.split('-', 1)
            if ':' in parts[1]:
                usr.append(line)
                u, s = 1, 0
            else:
                sys.append(line)
                s, u = 1, 0
        else:
            if s == 1 and u == 0:
                sys[-1] += ' ' + line.strip()
            elif s == 0 and u == 1:
                usr[-1] += ' ' + line.strip()

    # ===== Parse user messages =====
    user_data = []
    for k in usr:
        dt_nc = k.split(' - ')
        d_t = dt_nc[0].split(', ')
        n_c = dt_nc[1].split(': ')
        date, time_ = d_t[0], d_t[1]
        name, content = n_c[0], n_c[1]
        user_data.append((date, time_, name, content))

    # ===== Parse system messages =====
    system_data = []
    for m1 in sys:
        dt_c = m1.split(' - ')
        d_t = dt_c[0].split(', ')
        content = dt_c[1]
        date, time_ = d_t[0], d_t[1]
        system_data.append((date, time_, content))

    # ===== Display messages =====
    with st.expander("📄 User Messages"):
        st.write(user_data)
    with st.expander("⚙️ System Messages"):
        st.write(system_data)

    # ===== Most interactive user (dictionary method) =====
    d_0 = {}
    for _, _, username, _ in user_data:
        if username in d_0:
            d_0[username] += 1
        else:
            d_0[username] = 1

    # Find the top user manually
    max_count = 0
    top_user = ""
    for user, count in d_0.items():
        if count > max_count:
            max_count = count
            top_user = user

   

    # ===== Messages per user chart =====
    users = list(d_0.keys())
    counts = list(d_0.values())
    fig = px.bar(x=counts, y=users, orientation='h', text=counts,
                 color=users, title="📊 Messages per User", template="plotly_dark")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # ===== Top user badge =====
    st.subheader("👑 Most Interactive User")
    st.markdown(f"""
        <div style="background-color:#ffcc00;padding:15px;border-radius:10px;text-align:center">
            <h2>{top_user}</h2>
            <p style="font-size:18px">Messages Sent: <b>{max_count}</b></p>
            <p style="color:red;font-weight:bold;">🔥 Top Contributor</p>
        </div>
    """, unsafe_allow_html=True)

    # ===== Most used words ignoring media messages (without Counter) =====
    stop_words = set([
        "a","as","an","the","am","is","are","was","were","be","been","being",
        "i","me","my","mine","myself",
        "you","your","yours",
        "he","him","his",
        "she","her","hers",
        "it","its",
        "we","us","our","ours",
        "they","them","their","theirs",
        "and","or","but","nor","so","yet","because",
        "to","of","in","on","for","with","at","by","from",
        "this","that","these","those",
        "do","does","did","have","has","had",
        "can","could","will","would","should","may","might","must",
        "very","just","really","also","quite","too","enough",
        "who","whom","whose","which","what","while","when","where","why","how"
    ])
    media_phrases = ["<media omitted>", "<image omitted>", "<video omitted>", "<sticker omitted>"]

    # Combine all user messages into one string
    message_text = ""
    for u in user_data:
        content_lower = u[3].lower()
        if content_lower not in media_phrases:
            message_text += " " + content_lower

    words = [w.strip(string.punctuation) for w in message_text.split() if w.strip(string.punctuation) not in stop_words and w.strip(string.punctuation) != ""]

    # Count most frequent word manually
    word_count_dict = {}
    for w in words:
        if w in word_count_dict:
            word_count_dict[w] += 1
        else:
            word_count_dict[w] = 1

    max_word_count = 0
    most_used_words = []
    for word, count in word_count_dict.items():
        if count > max_word_count:
            max_word_count = count
            most_used_words = [word]
        elif count == max_word_count:
            most_used_words.append(word)

    # ===== Display most used words =====
    st.subheader("📝 Most Used Word(s)")
    st.markdown("<div style='display:flex;flex-wrap:wrap'>", unsafe_allow_html=True)
    for word in most_used_words:
        st.markdown(f'<span style="color:#00ff99;font-size:20px;padding:8px;margin:4px;border:2px solid #00ff99;border-radius:5px">{word}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:white;font-size:18px'>Used {max_word_count} times</p>", unsafe_allow_html=True)

    # ===== Timeline of messages =====
    timeline_data = []
    for u in user_data:
        dt = datetime.strptime(u[0] + ' ' + u[1], "%d/%m/%Y %I:%M %p")
        timeline_data.append(dt)

    # Count messages per hour manually
    timeline_count_dict = {}
    for dt in timeline_data:
        dt_hour = dt.replace(minute=0, second=0, microsecond=0)
        if dt_hour in timeline_count_dict:
            timeline_count_dict[dt_hour] += 1
        else:
            timeline_count_dict[dt_hour] = 1

    sorted_times = sorted(timeline_count_dict.keys())
    timeline_counts = [timeline_count_dict[t] for t in sorted_times]

    fig_timeline = px.line(x=sorted_times, y=timeline_counts, markers=True,
                           title="🕒 Messages Over Time", template="plotly_dark")
    fig_timeline.update_layout(xaxis_title="Time", yaxis_title="Number of Messages")
    st.plotly_chart(fig_timeline, use_container_width=True)
