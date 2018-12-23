import React, { Component } from 'react';
import { GoogleLogout } from 'react-google-login';

class Logout extends Component {
    logout() {
        // console.log(res)
        console.log('adit')
    }
    render() {
        return (
            <GoogleLogout
                buttonText="Logout"
                onSuccess={this.logout}
            >
            </GoogleLogout>
        )
    }
}

export default Logout;