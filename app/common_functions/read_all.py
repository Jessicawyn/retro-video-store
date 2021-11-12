

def read_all(model):
    all_data = model.query.all()

    response = []
    for data in all_data:
        response.append(
            data.to_dict()
        )
    return response