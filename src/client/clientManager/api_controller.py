from clientManager import app
from flask import jsonify, request, abort

studies = [
    {
        "id": "1",
        "title": "Bachelor Informatik",
        "description": "Ein toller Studiengang"
    },
    {
        "id": "2",
        "title": "Diplom Informatik",
        "description": "Das musst du studieren!"
    },
    {
        "id": "3",
        "title": "Master Informatik",
        "description": "Das kommt danach"
    }
]


@app.route('/test/api/studies', methods=['GET'])
def testapi1():
    return jsonify({
        "studies": studies
    })


@app.route('/test/api/study/<int:study_id>', methods=['GET'])
def testapi(study_id):
    return jsonify({"id": "1", "title": "Bachelor Informatik"})


@app.route('/test/api/study', methods=['PUT'])
def savestudy():
    if not request.json:
        abort(400)

    if request.json["id"]:
        studyid = int(request.json["id"])
    elif len(studies) != 0:
        studyid = int(studies[-1]["id"]) + 1
    else:
        studyid = 1

    study = {
        "id": studyid,
        "title": request.json["title"],
        "description": request.json["description"]
    }

    # remove entry with studyid
    studies[:] = [d for d in studies if d.get('id') != studyid]
    studies.append(study)

    print(studies)
    print(studyid - 1)

    return jsonify(studies[studyid - 1])
