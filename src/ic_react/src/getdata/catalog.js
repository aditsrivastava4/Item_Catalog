import React, { Component } from 'react';

class Catalog extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
        this.getData()
    }

    getData() {
        let data = [];
        fetch('/API/catalog.json')
            .then(catalogItem => catalogItem.json())
            .then((result) => {
                result.results.forEach(item => {
                    data.push(item.category)
                    // console.log(item.category)
                });
                this.setState({
                    isLoaded: true,
                    items: data
                })
            })

        // return data;
    }
    render() {
        // let res = this.getData();
        // let data = [12424,124,12,41,24,12,5,34,6,7,4,7,657]
        // console.log(res)
        const { error, isLoaded, items } = this.state;

        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div className="container">
                    <div className="row">
                        <div className="col-md-8">
                            <h1>Adit</h1>
                            {
                                items.map(function(d) {
                                    console.log(d)
                                    return <h1>{d}</h1>
                                })
                            }
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Catalog;
