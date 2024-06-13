import requests
import json

queryString = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      acRate
      difficulty
      freqBar
      frontendQuestionId: questionFrontendId
      isFavor
      paidOnly: isPaidOnly
      status
      title
      titleSlug
      topicTags {
        name
        id
        slug
      }
      hasSolution
      hasVideoSolution
    }
  }
}
"""


def fetch_data(limit, skip):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
    }

    variable_object = {
        "categorySlug": "",
        "limit": limit,
        "skip": skip,
        "filters": {}
    }

    payload = {
        "query": queryString,
        "variables": variable_object
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response)
