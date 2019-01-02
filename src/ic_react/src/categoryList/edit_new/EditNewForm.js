import React, { Component } from 'react';
import Cookies from 'js-cookie';

// Form Component for both Edit Item and Add a New Item
class EditNewForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loggedIn: Cookies.get('loggedIn'),
            isLoaded: this.props.option == "New"? true: false,
            error: null,
            option: this.props.option,
            itemData: this.props.itemData,
            categories: null,
            title: null,
            author: null,
            publisher: null,
            description: null,
            category: this.props.option == "New"? this.props.CategoryName: null
        }
        if(this.state.option == "Edit") {
            this.getData()
        }
        this.valueChange = this.valueChange.bind(this)
        this.submit = this.submit.bind(this)
    }

    getData() {
        let data = [];
        fetch('/API/catalog/category.json')
        .then(catalogItem => catalogItem.json())
        .then((result) => {
            result.results.forEach(item => {
                data.push(item.category)
            });
            this.setState({
                isLoaded: true,
                categories: data
            })
        })
    }

    submit(event) {
        const { title, author, publisher, description, category, itemData } = this.state
        let form_data = {
            title: title,
            author: author,
            publisher: publisher,
            description: description,
            category: category,
            uid: Cookies.get('uid')
        }
        let url;
        if(this.state.option == "Edit") {
            url = "/catalog/"+ itemData.item_id +"/edit"
        } else {
            url = "/catalog/"+ category +"/new"
        }

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(form_data)
        })
        .then((response) => {
            return response.json()
        })
        .then((result) => {
            if(result.code == 200 && result.item_ID == undefined) {
                this.props.afterUpdate()
            }
            if(result.code == 200 && result.item_ID != undefined) {
                this.props.afterUpdate()
            }
        })

        event.preventDefault()
    }

    valueChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
        event.preventDefault()
    }

    render() {
        const { itemData, option, categories, isLoaded, error } = this.state
        let opt = (option == "Edit" ? "Update" : "Add")
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-sm-2 col-md-2 col-lg-2"></div>
                        <div className="col-sm-8 col-md-8 col-lg-8 text-center">
                            <h3>{ this.state.option } Books Detail</h3>
                        </div>
                        <div className="col-sm-2 col-md-2 col-lg-2"></div>
                    </div>

                    <div className="row">

                        <div className="col-sm-2 col-md-2 col-lg-2"></div>

                        <div className="col-sm-8 col-md-8 col-lg-8 text-center">
                            <form onSubmit={ this.submit } className="form-horizontal">

                                <div className="form-group">
                                    <label className="control-label col-sm-2">Title:</label>
                                    <div className="col-sm-10">
                                        <input
                                            className="form-control"
                                            type="text"
                                            name="title"
                                            placeholder={ itemData.item }
                                            onChange={ this.valueChange } />
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="control-label col-sm-2">Author:</label>
                                    <div className="col-sm-10">
                                        <input
                                            className="form-control" 
                                            type="text" 
                                            name="author" 
                                            placeholder={ itemData.author }
                                            onChange={ this.valueChange } />
                                    </div>
                                </div>
                                
                                <div className="form-group">
                                    <label className="control-label col-sm-2">Publisher:</label>
                                    <div className="col-sm-10">
                                        <input 
                                            className="form-control" 
                                            type="text" 
                                            name="publisher" 
                                            placeholder={ itemData.publisher }
                                            onChange={ this.valueChange } />
                                    </div>
                                </div>


                                <div className="form-group">
                                    <label className="control-label col-sm-2">Description:</label>
                                    <div className="col-sm-10">
                                        <textarea
                                            className="form-control"
                                            type="text" 
                                            name="description"
                                            placeholder={ itemData.description }
                                            rows="4"
                                            cols="50"
                                            onChange={ this.valueChange }>
                                        </textarea>
                                    </div>
                                </div>


                                <div className="form-group">
                                    <label className="control-label col-sm-2">Category:</label>
                                    <div className="col-sm-10">
                                        { categories != null ?
                                            <select className="form-control" name="category" onChange={ this.valueChange }>
                                            {
                                                categories.map((category) => {
                                                    if(category == this.props.CategoryName) {
                                                        return (
                                                            <option selected>{ category }</option>
                                                        )
                                                    }
                                                    return (
                                                        <option>{ category }</option>
                                                    )
                                                }) 
                                            }
                                            </select> :
                                            <input 
                                                className="form-control" 
                                                type="text" 
                                                name="category" 
                                                value={ this.props.CategoryName }
                                                disabled/>
                                        }
                                    </div>
                                </div>


                                <div className="form-group">        
                                    <div className="col-sm-offset-2 col-sm-10">
                                        <input className="btn btn-default" type="submit" name={ opt } value={ opt } />
                                        &nbsp;
                                        <input className="btn btn-default" type="button" name="Cancel" value="Cancel" />
                                    </div>
                                </div>
                            </form>
                        </div>

                        <div className="col-sm-2 col-md-2 col-lg-2"></div>
                    </div>
                </div>
            )
        }
    }
}

export default EditNewForm;