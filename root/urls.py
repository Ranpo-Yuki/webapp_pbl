from controllers import * 
 
# FastAPIのルーティング用関数
app.add_api_route('/', index, methods=['GET', 'POST'])
app.add_api_route('/test', test, methods=['GET', 'POST'])
app.add_api_route('/DateSearch', DateSearch)
app.add_api_route('/NameSearch', NameSearch, methods=['GET', 'POST'])
app.add_api_route('/DisplayDate', DisplayDate)