keyword_pipeline = [
    {
        "$unwind": {
            "path": "$subscribed_keywords",
            "includeArrayIndex": "string",
            "preserveNullAndEmptyArrays": False,
        }
    },
    {
        "$lookup": {
            "from": "keyword_expansion",
            "localField": "subscribed_keywords.topic_name",
            "foreignField": "word_cluster",
            "as": "expansion",
        }
    },
    {
        "$project": {
            "reddit_username": 1,
            "is_public": 1,
            "subscription": {
                "$cond": {
                    "if": {
                        "$and": [
                            {"$eq": ["$subscribed_keywords.is_expanded", True]},
                            {"$gt": [{"$size": "$expansion"}, 0]},
                        ]
                    },
                    "then": {"$arrayElemAt": ["$expansion.word_cluster", 0]},
                    "else": ["$subscribed_keywords.topic_name"],
                }
            },
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "reddit_username": {"$first": "$reddit_username"},
            "is_public": {"$first": "$is_public"},
            "expanded_subscriptions": {"$push": "$subscription"},
        }
    },
]
