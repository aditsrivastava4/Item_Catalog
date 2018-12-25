import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';
import Cookies from 'js-cookie'

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            password: null,
            email: null,
            invalid: false,
            csrfToken: window.initialData
        };
        this.loginValue = this.loginValue.bind(this);
        this.login = this.login.bind(this);
    }

    loginValue(event) {
        // change state of each value
        this.setState({
            [event.target.name]: event.target.value
        })
    }
    login(event) {
        fetch('/login', {
            method: 'post',
            body: JSON.stringify(this.state)
        })
        .then((response) => {
            return response.json()
        })
        .then((response) => {
            if(response.LoggedIn) {
                Cookies.set('username', response.username)
                Cookies.set('loggedIn', true)
                Cookies.set('type', 'local')
                Cookies.set('uid', response.csrfToken)

                setTimeout(function() {
                    window.location.href = "/";
                }, 500);
            } else if(!response.user_exist) {
                this.setState({
                    invalid: true
                })
            }
        })
        event.preventDefault()
    }

    successG_OAuth(response) {
        console.log(response);
        response.csrfToken = this.state.csrfToken
        console.log(response);
        fetch(
            '/G_OAuth',
            {
                method: 'post',
                body: JSON.stringify(response)
            })
            .then((gOAuth) => {
                return gOAuth.json();
            }).then((data) => {
                if(data.LoggedIn) {
                    Cookies.set('username', response.profileObj.name)
                    Cookies.set('loggedIn', true)
                    Cookies.set('type', 'G_OAuth')
                    Cookies.set('uid', data.csrfToken)

                    setTimeout(function() {
                        window.location.href = "/";
                    }, 500);
                }
            });
    }
    failG_OAuth(response) {
        console.log(response);
        alert("Google Login Failed!")
        setTimeout(function() {
            window.location.href = "/login";
        }, 500);
    }

    render() {
        const { email, password, invalid } = this.state
        return (
            <div className="col-sm-6 col-md-6 col-lg-6">
                <form onSubmit={this.login}>
                    {/* <!-- For CSFR Protection --> */}
                    {/* <input type='hidden' name='state' value='{{ STATE }}' /> */}
                    <label>Email:</label>
                    <input
                        className="form-control"
                        id="email"
                        type="text"
                        name="email"
                        value={ email }
                        onChange={ this.loginValue } /><br />
        
                    <label>Password:</label>
                    <input
                        className="form-control"
                        id="pwd" 
                        type="password"
                        name="password"
                        value={ password }
                        onChange={ this.loginValue } /><br />

                    { invalid? <p className="text-danger">*Invalid Email or Password</p> : ""}

                    <input className="btn btn-default" type="submit" name="Login" value="Login" />
                </form>
        
                <h5 className="text-center"><strong>OR</strong></h5>

                <div className="row">
                    <div className="col-sm-12 col-md-12 col-lg-12 text-center" id="signinButton">
                    <GoogleLogin
                        clientId="186601709381-8ju1gc3e2v7lube266nn1hrgrmqtunvr.apps.googleusercontent.com"
                        buttonText="Login"
                        onSuccess={this.successG_OAuth}
                        onFailure={this.failG_OAuth}
                    />
                    </div>
                </div>

            </div>
        );
    }
}

export default LoginForm;
