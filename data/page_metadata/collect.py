import csv

csv_paths = ["l1p1", "l1p2", "l2p1", "l2p2"]

for p in csv_paths:
	csv_path = p + "_pages.csv"
	print(csv_path)
	with open(csv_path, newline="", encoding="utf-8-sig") as f:
		reader = csv.DictReader(f)
		rows = list(reader)
		for i,row in enumerate(rows):
			start = int(row["core_vocab_start_page_pdf"])
			end = start + 4
			end_s = "," if i < len(rows) - 1 else "\n"
			print(f"{start}-{end}", end=end_s)

