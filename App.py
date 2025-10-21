import streamlit as st
import json
import base64
from io import BytesIO

st.set_page_config(page_title="🎬 VEO3 Prompt Generator", page_icon="🎥", layout="wide")

st.title("🎬 VEO3 Prompt Generator")
st.markdown("Buat prompt video otomatis untuk VEO3 lengkap dengan struktur JSON yang bisa langsung disalin.")

st.divider()

# Form Input
with st.form("veo3_form"):
    st.header("🧩 Informasi Utama")
    project_name = st.text_input("Nama Proyek / Produk", placeholder="Contoh: Review Parfum Dominant")
    scene_count = st.number_input("Jumlah Scene", min_value=1, max_value=10, value=2)
    voice_type = st.selectbox("Tipe Suara Voice Over", ["Pria", "Wanita"])
    tone = st.selectbox("Nada Bicara", ["Lembut", "Bersemangat", "Meyakinkan", "Santai"])
    style = st.text_area("Gaya Video / Visual", placeholder="Contoh: clean minimalis, aesthetic, elegan, natural lighting")

    uploaded_images = st.file_uploader("Tambahkan Gambar (opsional)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    st.divider()
    st.header("🎬 Detail Tiap Scene")

    scenes = []
    for i in range(scene_count):
        st.subheader(f"Scene {i+1}")
        scene_desc = st.text_area(f"Deskripsi Scene {i+1}", placeholder="Contoh: Kamera statis, menyorot produk di atas meja kayu dengan pencahayaan lembut.", key=f"desc_{i}")
        voice_text = st.text_area(f"Voice Over Scene {i+1}", placeholder="Contoh: Ini dia parfum yang bikin kamu tampil percaya diri seharian!", key=f"voice_{i}")
        scenes.append({
            "scene": i+1,
            "description": scene_desc,
            "voice_over": voice_text
        })

    submitted = st.form_submit_button("🚀 Generate Prompt")

# Output JSON
if submitted:
    st.success("✅ Prompt berhasil dibuat!")
    
    # Encode images (base64)
    encoded_images = []
    for img in uploaded_images:
        bytes_data = img.read()
        encoded = base64.b64encode(bytes_data).decode('utf-8')
        encoded_images.append({
            "filename": img.name,
            "base64": encoded
        })

    result = {
        "project": project_name,
        "voice": {
            "gender": voice_type,
            "tone": tone
        },
        "visual_style": style,
        "scenes": scenes,
        "images": encoded_images if uploaded_images else "Tidak ada gambar diunggah"
    }

    json_result = json.dumps(result, indent=4, ensure_ascii=False)

    st.divider()
    st.subheader("📄 Hasil JSON Prompt")
    st.code(json_result, language="json")

    # Tombol salin
    st.download_button(
        label="📋 Salin / Unduh JSON Prompt",
        data=json_result.encode('utf-8'),
        file_name=f"{project_name.replace(' ', '_')}_prompt.json",
        mime="application/json"
    )

st.divider()
st.markdown("💡 *Dibuat oleh Mulmulmuk95 untuk pembuatan prompt otomatis VEO3.*")
