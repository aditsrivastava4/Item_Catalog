import React, { Component } from 'react';
import Cookies from 'js-cookie';

class EditItem extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: false,
            error: null
        }
    }
    render() {
        return (
            <div></div>
        )
    }
}

export default EditItem;