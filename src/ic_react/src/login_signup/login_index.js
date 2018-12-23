import React, { Component } from 'react';
import Navbar from '../navbar/navbar'
import LoginForm from './login_form'
import Cookies from 'js-cookie'
import { Redirect } from 'react-router-dom'

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loggedIn: Cookies.get('loggedIn')
        };
    }
    render() {
        const { loggedIn } = this.state
        if(loggedIn) {
            return (
                // Redirect to Home page if logged In
                <Redirect to="/" />
            )
        }
        // else render the login component
        return (
            <div>
                <Navbar />
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-12 col-lg-12 text-center">
                            <h3>Login</h3>
                        </div>
                        <div className="col-sm-3 col-md-3 col-lg-3"></div>
                        <LoginForm />
                        <div class="col-sm-3 col-md-3 col-lg-3"></div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Login;
