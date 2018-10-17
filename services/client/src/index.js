import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import AddUser from './components/AddUser';

class App extends Component {
  constructor() {
    super();
    this.state = { email: '', password: ''};
    this.addUser = this.registerUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
  };

  handleChange(event) {
  const obj = {};
  obj[event.target.name] = event.target.value;
  this.setState(obj);
  };

  registerUser(event) {
    event.preventDefault();
    console.log('sanity check!');
    const data = {
      email: this.state.email, password: this.state.password
    };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users` , data)
  .then(function (response) {
    console.log(response.data.message);
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
              <h1 className="title is-1">Register to AP</h1>
              <hr/><br/>
              <AddUser email={this.state.email} password={this.state.password}
                handleChange={this.handleChange} addUser={this.addUser}/>
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
