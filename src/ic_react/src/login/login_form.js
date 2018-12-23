import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';
import Cookies from 'js-cookie'

class LoginForm extends Component {
    successG_OAuth(response) {
        console.log(response);
        fetch(
            '/G_OAuth',
            {
                method: 'post',
                body: JSON.stringify(response.profileObj)
            })
            .then((gOAuth) => {
                return gOAuth.json();
            }).then((data) => {
                if(data.LoggedIn) {
                    // document.cookie = "username=" + response.profileObj.name
                    // document.cookie = "loggedIn=True"
                    // document.cookie = "type=G_OAuth"
                    Cookies.set('username', response.profileObj.name)
                    Cookies.set('loggedIn', true)
                    Cookies.set('type', 'G_OAuth')

                    setTimeout(function() {
                        window.location.href = "/";
                    }, 500);
                }
            });
    }
    failG_OAuth(response) {
        console.log(response);
    }

    render() {
        return (
            <div className="col-sm-6 col-md-6 col-lg-6">
                <form method="POST">
                    {/* <!-- For CSFR Protection --> */}
                    {/* <input type='hidden' name='state' value='{{ STATE }}' /> */}
                    <label>Email:</label>
                    <input className="form-control" id="email" type="text" name="email" /><br />
        
                    <label>Password:</label>
                    <input className="form-control" id="pwd" type="password" name="password" /><br />

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
