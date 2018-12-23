import React, { Component } from 'react';
import Navbar from '../navbar/navbar'
import LoginForm from './login_form'

class Login extends Component {
    render() {
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
