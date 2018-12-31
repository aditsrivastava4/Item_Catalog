import React, { Component } from 'react';
import Cookies from 'js-cookie';
import EditNewForm from './EditNewForm';

class EditNew_index extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            option: this.props.option
        }
    }
    render() {
        return (
            <EditNewForm option = { "edit" }/>
        )
    }
}

export default EditNew_index;