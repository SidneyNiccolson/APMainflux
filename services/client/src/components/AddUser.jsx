import React from 'react';

const AddUser = (props) => {
  return (
    <form onSubmit={ (event) => props.addUser(event) }>
      <div className="field">
      <div className="field">
        <input
          name="email"
          className="input is-small"
          type="email"
          placeholder="Enter an email address"
          required
          value={props.email}
          onChange={props.handleChange}
        />
      </div>
      <input
        name="password"
        className="input is-small"
        type="password"
        placeholder="Enter a password"
        required
        value={props.password}
        onChange={props.handleChange}
      />
      </div>
      <input
        type="submit"
        className="button is-primary is-small is-fullwidth"
        value="Submit"
      />
    </form>
  )
};

export default AddUser;
