import React, { Component } from 'react';
import Navbar from '../navbar/navbar';
import Cookies from 'js-cookie'
import { Redirect } from 'react-router-dom'

class SignUp extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            username: null,
            password: null,
            email: null
        };
        this.signUpValue = this.signUpValue.bind(this);
        this.signUp = this.signUp.bind(this);
    }
    signUpValue(event) {
        // change state of each value
        this.setState({
            [event.target.name]: event.target.value
        })
    }
    signUp(event) {
        fetch('/signup', {
            method: 'post',
            body: JSON.stringify(this.state)
        })
        .then((response) => {
            return response.json()
        })
        .then((response) => {
            if(response.LoggedIn) {
                Cookies.set('username', this.state.username)
                Cookies.set('loggedIn', true)
                Cookies.set('type', 'local')
                Cookies.set('uid', response.csrfToken)
                
                setTimeout(function() {
                    window.location.href = "/";
                }, 500);
            }
        })
        event.preventDefault()
    }
    render() {
        const { loggedIn, username, password, email } = this.state
        if(loggedIn) {
            return (
                // Redirect to Home page if logged In
                <Redirect to="/" />
            )
        }
        // else render the SignUp component
        return (
            <div>
                <Navbar />
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                            <h3>Sign Up</h3>
                        </div>
                        <div className="col-sm-2 col-md-2 col-lg-2"></div>

                        <div className="col-sm-8 col-md-8 col-lg-8">

                            <form onSubmit={this.signUp}>
                                <label>Name:</label>
                                <input
                                    className="form-control"
                                    type="text"
                                    name="username"
                                    value={ username }
                                    onChange={this.signUpValue} /><br />

                                <label>Email:</label>
                                <input
                                    className="form-control"
                                    id="email"
                                    type="text"
                                    name="email"
                                    value={ email }
                                    onChange={this.signUpValue} /><br />

                                <label>Password:</label>
                                <input
                                    className="form-control"
                                    id="pwd"
                                    type="password"
                                    name="password"
                                    value={ password }
                                    onChange={this.signUpValue} /><br />

                                <input className="btn btn-default" type="submit" name="Sign Up" value="Sign Up" />
                            </form>
                        </div>
                        <div className="col-sm-2 col-md-2 col-lg-2"></div>
                    </div>
                </div>
            </div>
        )
    }
}

export default SignUp;