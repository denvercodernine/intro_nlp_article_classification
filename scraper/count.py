import csv
cat_ids = {1001005: "Thời sự", 1001002: "Thế giới", 1003159: "Kinh doanh", 1002691: "Giải trí", 1002565: "Thể thao",
           1001007: "Pháp luật", 1003497: "Giáo dục", 1003750: "Sức khỏe", 1002966: "Đời sống", 1003231: "Du lịch", 1001009: "Khoa học"}
cat_ids_list = list(cat_ids.keys())
success = []
failure = []


class counter:
    def __init__(self):
        self.cat_list = []
        for key in cat_ids:
            self.cat_list.append(0)

    def add(self, cat_id):
        if cat_id in cat_ids.keys():
            self.cat_list[list(cat_ids.keys()).index(cat_id)]+=1
    def print(self):
        for key in cat_ids.keys():
            print(f"{cat_ids[key]}: {self.cat_list[list(cat_ids.keys()).index(key)]}")

ctr = counter()

with open('scraper\\newdata.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            print(
                f"Title: {row['title']}\nCategory: { cat_ids[int(row['catidbase'])] }")
            print("-"*10)
            success.append(row['postid'])
            ctr.add(int(row['catidbase']))
        except Exception as err:
            print(f"Error: {err}, category: {row['catid']}, tree: {row['catidlist']}")
            failure.append(row['postid'])
print(f"{len(success)} out of {len(success)+len(failure)} articles were recognized.")
print("Composition:")
ctr.print()