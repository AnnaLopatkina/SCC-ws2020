# Service and Cloud Computing Projekt - Gruppe 10

---

## Gruppe:

Anna Lopatkina

Ella Hirche

Fabian Wolf @FWao

---

## Dokumentation

[Dokumentation](https://bitbucket.org/tudresden/ws2020-gruppe10/src/master/doku.pdf)

[Study Service API](https://bitbucket.org/tudresden/ws2020-gruppe10/src/master/output-study.pdf)

[User Service API](https://bitbucket.org/tudresden/ws2020-gruppe10/src/master/output-user.pdf)

---

## How to run client in docker with certs

Docker client: docker run -d --network rest-net --name webclient -p 443:443 --mount type=bind,source=/home/debian/certs,target=/certs fwao/webclient
