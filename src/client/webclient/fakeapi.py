from flask import jsonify, request, abort

from webclient import app

studies = [
    {
        "id": "1",
        "title": "Bachelor Informatik",
        "description": "Ein toller Studiengang",
        "semesters": "6",
    },
    {
        "id": "2",
        "title": "Diplom Informatik",
        "description": "Das musst du studieren!",
        "semesters": "10",
    },
    {
        "id": "3",
        "title": "Master Informatik",
        "description": "Das kommt danach",
        "semesters": "4",
    }
]


@app.route('/test/api/studies', methods=['GET'])
def testapi1():
    return jsonify({
        "studies": studies
    })


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


study = {
    "id": "1",
    "title": "Bachelor Informatik",
    "semesters": "6",
    "modules": [
        {
            "id": "1",
            "title": "Mathematik für Informatiker 1",
            "semester": "1",
            "lectures": [
                {
                    "id": "1",
                    "title": "Lineare Algebra",
                    "semester": "1",
                    "responsible": "Prof Baumann"
                },
                {
                    "id": "2",
                    "title": "Diskrete Strukturen",
                    "semester": "1",
                    "responsible": "Prof Bodirsky"
                }
            ]
        },
        {
            "id": "2",
            "title": "Rechnerarchitektur",
            "semester": "1",
            "lectures": [
                {
                    "id": "1",
                    "title": "Rechnerarchitektur 1",
                    "semester": "3",
                    "responsible": "Prof Baumann"
                },
                {
                    "id": "2",
                    "title": "Rechnerarchitektur 2",
                    "semester": "4",
                    "responsible": "Prof Bodirsky"
                }
            ]
        }
    ]
}


@app.route('/test/api/study/<int:studyid>', methods=['GET'])
def getstudy(studyid):
    print("endpoint getstudy with id {}".format(studyid))
    return jsonify({"study": study})
