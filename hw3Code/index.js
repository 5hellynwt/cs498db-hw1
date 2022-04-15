const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const {spawn} = require('child_process');

const app = express()
app.use(bodyParser.json());

app.get('/', (req, res) => {
        res.json({"Hello": "World"});
});

app.get('/lengthCounts', (req, res) => {
        fs.readFile('/home/g5hellyn_uuilliam/project/output/merged', 'utf8', (err, data) => {
                if (err) {
                        console.error(err);
                } else {
                        wordsLength = {}
                        var lines = data.split('\n');
                        lines.pop();

                        for (var i in lines) {
                                line = lines[i].split(', ');
                                left = line[0].slice(1);
                                right = line[1].slice(0, -1);

                                wordsLength[left] = parseInt(right);
                        }

                        res.json(wordsLength);
                }
        });

});

app.post('/analyze', (req, res) => {
        let wl = req.body.wordlist;
        let w = req.body.weights;
        const python = spawn('python3', ['spark_analyze.py', wl, JSON.stringify(w), 'analyzed']);
         python.stdout.on('data', function (data) {
                console.log(data.toString());
        });

        python.stderr.on('data', function(data) {
                console.log(data.toString());
        });

        res.json("Processing..");
});

app.get('/result', (req, res) => {
        if (fs.existsSync("analyzed/merged")) {
                fs.readFile('analyzed/merged', 'utf8', (err, data) => {
                        wordLines = {}
                        var lines = data.split('\n');
                        lines.pop();

                        for (var i in lines) {
                                line = lines[i].split("', ");
                                left = line[0].slice(2);
                                right = line[1].slice(1);

                                wordLines[left] = right;
                        }

                        res.json(wordLines);
                });
        } else {
                res.json("Not done yet");
        }
});

var http = require('http').Server(app);

const PORT = 80;
http.listen(PORT, function() {
        console.log("Listening..");
});
