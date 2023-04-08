const express = require('express')
const mysql = require('mysql')
const app = express()
const cors = require('cors')

app.use(cors())
app.use(express.json())

const db = mysql.createConnection({
    user: "admin",
    password: "password",
    port: "port,
    host: "host",
    database: "Obey Clan"
})

app.post("/create", (req, res) => {
    console.log("-----")
    console.log(req.body)
    const id = req.body.id
    const discordid = req.body.discordid
    const discordname = req.body.discordname
    const pgid = req.body.pgid
    const pgname = req.body.pgname
    const rank = req.body.rank
    const valors = req.body.valors

    db.query("INSERT INTO members VALUES(?,?,?,?,?,?,?)",
    [id, discordid, discordname, pgid, pgname, rank, valors], (err, result) => {
        if (err) {
            console.log(err)
        } else {
            res.send("Values inserted")
        }
    })
})

app.get("/get", (req, res) => {
    db.query("SELECT * FROM members", (err, result) => {
        if (err) {
            console.log(err)
        } else {
            res.send(result)
        }
    })
})

app.listen(3001, () => {
    console.log("Your server on!")
})
