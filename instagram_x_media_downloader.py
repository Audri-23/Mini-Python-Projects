import gallery_dl

url = input("Enter Instagram or Twitter/X post URL: ")
gallery_dl.job.DownloadJob(url).run()

print("Download completed! Check the 'gallery-dl' folder.")
