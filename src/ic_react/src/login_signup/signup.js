import React, { Component } from 'react';
import Navbar from '../navbar/navbar';

class SignUp extends Component {
    signUp() {
    }
    render() {
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

                            <form method="POST">
                                <label>Name:</label>
                                <input className="form-control" type="text" name="username" /><br />

                                <label>Email:</label>
                                <input className="form-control" id="email" type="text" name="email" /><br />

                                <label>Password:</label>
                                <input className="form-control" id="pwd" type="password" name="password" /><br />

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