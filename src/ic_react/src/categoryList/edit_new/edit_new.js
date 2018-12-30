import React, { Component } from 'react';
import Cookies from 'js-cookie';
import EditItem from './editItem';
import NewItem from './newItem';

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
            <div>
                { this.state.option == 'edit' ?
                    <EditItem /> :
                    <NewItem />
                }
            </div>
        )
    }
}

export default EditNew_index;