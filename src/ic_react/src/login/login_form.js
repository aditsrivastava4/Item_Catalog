import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';

class LoginForm extends Component {
    successG_OAuth(response) {
        console.log(response);
        fetch(
            '/G_OAuth',
            {
                type: 'POST'
            })
            .then(catalogItem => catalogItem.json())
            .then((result) => {
                result.results.forEach(item => {
                    data.push(item.category)
                });
                this.setState({
                    isLoaded: true,
                    items: data
                })
            })
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
        
                    {/* <p style="color: red;display:none;" >* Invalid username or password</p>
                    {% with messages = get_flashed_messages() %}
                        {% if messages %}
                                {% for message in messages %}
                                    <p style="color: red;">* {{ message }}</p>
                                {% endfor %}
                        {% endif %}
                    {% endwith %} */}
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
