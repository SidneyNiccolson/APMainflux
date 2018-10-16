import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

class App extends Component {
  constructor() {
    super();
    this.registerUser();
  }
  registerUser() {
  axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users` , {
    email: 'generic_user@guser.org',
    password: 'mypass'
  })
  .then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br/>
              <h1 className="title is-1">All Users</h1>
              <hr/><br/>
            </div>
          </div>
        </div>
      </section>
    )
  }
};


ReactDOM.render(
  <App />,
  document.getElementById('root')
);

