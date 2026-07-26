import speedtest

st = speedtest.Speedtest()

#For download speed
print("Checking Download Speed...")
download_speed = st.download()/1_000_000
print(f"Download Speed: {download_speed:.2f} Mbps")

#for upload speed
print("Checking upload Speed...")
upload_speed = st.upload()/1_000_000
print(f"Upload Speed: {upload_speed:.2f} Mbps")