import time
import csv
import requests
from datetime import datetime, timedelta
import json



def write_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


# define GraphQL endpoint
from exceptiongroup import catch

url = 'https://api.producthunt.com/v2/api/graphql'

# setup headers with API token
headers = {
    'Authorization': 'Bearer TSEO6kd29X0dmjWnD71fCtUA_EcZ6Cd8XtXanDS1AYA',  # replace with your token
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

# prepare the date seven days ago
# seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d") % seven_days_ago

today = datetime.today()
print(str(today))
# define GraphQL query

initial_query = """
{
  posts(order: FEATURED_AT, featured: true, createdAfter: 2023-07-11T00:00:00Z) {
    edges {
      node {
        id
        name
        description
        website
        votesCount 
        commentsCount
        createdAt
        featuredAt
      }
    }
    pageInfo{
        startCursor 
        endCursor 
        hasNextPage 
        hasPreviousPage 
    }
    totalCount
  }
}
"""
productList = []
#
decoder = json.JSONDecoder()
response = requests.post(url, headers=headers, json={'query': initial_query})
print(response.text)
resp = decoder.decode(response.text)
hasNextPage = resp.get('data').get('posts').get('pageInfo').get('hasNextPage')
startCursor = resp.get('data').get('posts').get('pageInfo').get('startCursor')
index = 0

try:
    while hasNextPage:
        query = """
        {
          posts(order: FEATURED_AT, featured: true, createdAfter:2023-07-11T00:00:00Z, after:\"""" + startCursor + """\",) {
            edges {
              node {
                id
                name
                description
                website
                votesCount 
                commentsCount
                createdAt
                featuredAt
              }
            }
            pageInfo{
                startCursor 
                endCursor 
                hasNextPage 
                hasPreviousPage 
            }
            totalCount
          }
        }
        """
        response = requests.post(url, headers=headers, json={'query': query})
        resp = decoder.decode(response.text)
        hasNextPage = resp.get('data').get('posts').get('pageInfo').get('hasNextPage')
        startCursor = resp.get('data').get('posts').get('pageInfo').get('startCursor')
        responseData = resp.get('data').get('posts').get('edges')
        for item in responseData:
            if item.get('node') not in productList:
                productList.append(item.get('node'))
        time.sleep(5)
        index += 1
        print(index)

except Exception:
    write_to_csv(productList, "productList.csv")

print(productList)

write_to_csv(productList, "productList.csv")
