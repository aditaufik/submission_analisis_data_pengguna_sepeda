import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Tema seaborn
sns.set_theme(style="dark")

# Function untuk memuat data
@st.cache_data
def load_data():
    #file local
    #df = pd.read_csv("day.csv")
    #file github
    df = pd.read_csv("Dashboard/day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df = df[(df['dteday'] >= '2011-01-01') & (df['dteday'] <= '2012-12-31')]
    return df

# Memuat data
day_df = load_data()

# Sidebar filter
st.sidebar.title("Filter Tahun")
pilihan_tahun = st.sidebar.radio( "Pilih Tahun", options=["2011", "2012", "Semua"]
)

# Pengkondisian untuk filter berdasarkan pilihan tahun
if pilihan_tahun == "2011":
    filtered_df = day_df[day_df['dteday'].dt.year == 2011]
    pilih = 2011
elif pilihan_tahun == "2012":
    filtered_df = day_df[day_df['dteday'].dt.year == 2012]
    pilih = 2012
else:
    filtered_df = day_df
    pilih = "2011 dan 2012"

st.header("Dashboard Pengguna Sepeda")
# Visualisasi Jumlah Pengguna Berdasarkan Musim
label_musim = ["Semi", "Panas", "Gugur", "Dingin"]
filtered_df['label_musim'] = filtered_df['season'].map({1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"})
pengguna_per_musim = filtered_df.groupby('label_musim')['cnt'].sum().reindex(label_musim)

st.subheader("Jumlah Pengguna Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=pengguna_per_musim.index, y=pengguna_per_musim.values, color='#00b2ff', ax=ax)
ax.set_title(f"Jumlah Pengguna Sepeda Berdasarkan Musim ({pilih})", fontsize=16)
ax.set_xlabel("Musim", fontsize=14)
ax.set_ylabel("Jumlah Pengguna (cnt)", fontsize=14)
st.pyplot(fig)

# Visualisasi Perbandigan Hari Kerja dan Libur
filtered_df['label_workingday'] = filtered_df['workingday'].map({0: "Hari Libur", 1: "Hari Kerja"})
pengguna_harikerja = filtered_df.groupby(['yr', 'label_workingday'])['cnt'].sum().unstack()

st.subheader("Perbandingan Penggunaan Sepeda pada Hari Kerja dan Hari Libur")
fig, ax = plt.subplots(figsize=(8, 6))
pengguna_harikerja.plot(kind='bar', ax=ax, color=['#ff9378', '#00b2ff'])

# Perubahan label tahun
ax.set_xticks(range(len(pengguna_harikerja.index)))
ax.set_xticklabels(pengguna_harikerja.index.map(lambda x: str(2011 + x)), rotation=0, fontsize=10)

ax.set_title(f"Perbandingan Penggunaan Sepeda pada Hari Kerja\n dan Hari Libur Berdasarkan Tahun ({pilih})", fontsize=14)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=12)
st.pyplot(fig)

# Visualissi Rata-rata Penggunaan Sepeda Tiap Bulan
st.subheader(f"Rata-rata Penggunaan Sepeda Tiap Bulan ({pilih})")

fig, ax = plt.subplots(figsize=(10, 6))

if pilihan_tahun == "Semua":
    # Jika pilih "Semua"
    pengguna_bulanan = day_df.groupby(['yr', 'mnth'])['cnt'].mean().unstack()
    for year in pengguna_bulanan.index:
        ax.plot(
            pengguna_bulanan.columns,
            pengguna_bulanan.loc[year],
            marker='o',
            label=f"Tahun {year}"
        )
    ax.set_title("Rata-rata Penggunan Sepeda Tiap Bulan (2011 dan 2012)", fontsize=16)
else:
    # Jika pilih salah satu tahun
    pengguna_bulanan = filtered_df.groupby(filtered_df['dteday'].dt.month)['cnt'].mean()
    ax.plot(
        pengguna_bulanan.index,
        pengguna_bulanan.values,
        marker='o',
        color='#00b2ff',
        label=f"Tahun {pilih}"
    )
    ax.set_title(f"Rata-rata Penggunaan Sepeda Tiap Bulan ({pilih})", fontsize=16)

# Pengaturan sumbu x dan y
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata Pengguna (cnt)", fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
    "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
])
ax.legend(title="Tahun", fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# Statistik tambahan
st.sidebar.subheader("Statistik Pengguna Sepeda")
st.sidebar.write(f"Rata-rata Pengunaan Sepeda ({pilih}): {filtered_df['cnt'].mean():.2f}")
st.sidebar.write(f"Total Pengguna Sepeda ({pilih}): {filtered_df['cnt'].sum():,.0f}")
