'use strict';

const {ipcRenderer} = require('electron')




function login(username, password) {
  document.getElementById("status").innerHTML = ""; //remove error message if there is one

  const axios = require('axios')

  var user = username //this should be a global variable for use in getNonFollowers()
  var pass = password

  console.log("Logging in...");

  axios.post('http://157.230.215.239:5000/login', {
    Username: user,
    Password: pass
  }).then(function (response) {
    //success
    console.log(response);
    loginStatus(response.data.logged)
  }).catch(function (error) {
    //failure
    console.log(error);
  });
}

function loginStatus(status) {
  if(status) {
    ipcRenderer.send('login');
  } else {
    document.getElementById("status").innerHTML = "Login failed. Try again!";
  }
}

function getNonFollowers() {
  console.log("Let's get the followers...")
  console.log(window.user)

  const axios = require('axios')

  axios.get('http://157.230.215.239:5000/nonfollowers')
  .then(function (response) {
    console.log(response)
    document.getElementById("status").innerHTML = "Here are the people not following you back:";

    var names = response.data;
    for (var username in names) {
        console.log("Adding divs...")

        var nonFollower = document.createElement('div');
        nonFollower.className = 'innerDiv';
        document.getElementById("container").appendChild(nonFollower);

        var nameText = document.createTextNode(names[username]);
        var usernameText = document.createTextNode(username);

        var nameP = document.createElement("p");
        nameP.className = "name";

        var usernameP = document.createElement("p");
        usernameP.className = "username";

        usernameP.appendChild(usernameText);
        nameP.appendChild(nameText);

        nonFollower.appendChild(usernameP);
        nonFollower.appendChild(nameP);
    }

  }).catch(function (error) {
    console.log(error)
  });
}
