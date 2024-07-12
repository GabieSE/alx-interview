#!/usr/bin/node

const request = require('request');

const movieId = process.argv[2];

if (!movieId) {
  console.error('Error: No movie ID provided');
  process.exit(1);
}

const filmEndPoint = 'https://swapi-api.hbtn.io/api/films/' + movieId;
let people = [];
const names = [];

const requestCharacters = async () => {
  await new Promise(resolve => request(filmEndPoint, (err, res, body) => {
    if (err) {
      console.error('Request Error:', err);
      process.exit(1);
    }
    if (res.statusCode !== 200) {
      console.error('Error: StatusCode:', res.statusCode);
      process.exit(1);
    }
    const jsonBody = JSON.parse(body);
    people = jsonBody.characters;
    resolve();
  }));
};

const requestNames = async () => {
  if (people.length > 0) {
    for (const p of people) {
      await new Promise(resolve => request(p, (err, res, body) => {
        if (err) {
          console.error('Request Error:', err);
        } else if (res.statusCode !== 200) {
          console.error('Error: StatusCode:', res.statusCode, 'URL:', p);
        } else {
          const jsonBody = JSON.parse(body);
          names.push(jsonBody.name);
        }
        resolve();
      }));
    }
  } else {
    console.error('Error: Got no characters for some reason');
  }
};

const getCharNames = async () => {
  await requestCharacters();
  await requestNames();

  for (const n of names) {
    process.stdout.write(n + '\n');
  }
};

getCharNames();
