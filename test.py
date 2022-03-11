from cursepy import CurseClient

client = CurseClient()
search = client.get_search()
search.pageSize = 5
search.searchFilter = "witchery"
for i in client.search(432, client.ADDON_SEARCH, search):
    print(i.name)
