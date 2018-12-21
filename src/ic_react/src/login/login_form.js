import React, { Component } from 'react';

class LoginForm extends Component {
    render() {
        const $ = window.$;
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
                    <div className="col-sm-6 col-md-6 col-lg-6" id="signinButton">
                        <span className="g-signin"
                            data-scope="openid email"
                            data-clientid="186601709381-8ju1gc3e2v7lube266nn1hrgrmqtunvr.apps.googleusercontent.com"
                            data-redirecturi="postmessage"
                            data-accesstype="offline"
                            data-cookiepolicy="single_host_origin"
                            data-callback="signInCallback"
                            data-approvalprompt="force">
                        </span>
                    </div>
                    <script /*type="text/javascript"*/
                        dangerouslySetInnerHTML={{__html: 
                            function signInCallback(authResult) {
                                if (authResult['code']) {
                                    // Hide the sign-in button now that the user is authorized
                                    $('#signinButton').attr('style', 'display: none');
                                    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
                                    $.ajax({
                                        type: 'POST',
                                        url: '/G_OAuth?state={{STATE}}',
                                        processData: false,
                                        data: authResult['code'],
                                        contentType: 'application/octet-stream; charset=utf-8',
                                        success: function(result) {
                                            // Handle or verify the server response if necessary.
                                            if (result) {
                                                    setTimeout(function() {
                                                    window.location.href = "/";
                                                }, 500);

                                            } else if (authResult['error']) {
                                                console.log('There was an error: ' + authResult['error']);
                                            } else {
                                                $('#result').html('Failed to make a server-side call. Check your configuration and console.');
                                            }
                                        }

                                    });
                                }
                            }
                        }}>
                    </script>
                </div>

            </div>
        );
    }
}

export default LoginForm;
