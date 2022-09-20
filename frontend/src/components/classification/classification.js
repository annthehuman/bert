import React, {Component} from 'react';
import Box from '@mui/material/Box';
import LoadingButton from '@mui/lab/LoadingButton';
import {TextField} from '@mui/material';
import {Stack} from '@mui/material';

export default class Classification extends Component {
    constructor(props){
        super(props);
        this.state ={
            text: '',
            token: '',
            loading: false
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleClick = this.handleClick.bind(this)
    }
  handleChange(event) {
    this.setState({text: event.target.value});
  }
  handleClick() {
    this.setState({loading: true});
  }
  handleSubmit(event) {
    // alert('A username and password was submitted: ' + this.state.username + " " + this.state.password);
    this.setState({loading: true});
    event.preventDefault();
    console.log(JSON.stringify({
        text: this.state.text
    }))
    let params = new URLSearchParams();
    params.append('text', this.state.text);

    fetch('/classificate', {
        method: "POST",
        body: params
        }).then(data => {
            if (!data.ok){
                data.json()
                .then(data =>{
                    console.log(data)
                    this.setState({errorLogin: data})       
                    throw Error(data);})
            } else {
                const result =  data.json() 
                return result}
        }).then(result => {
            // localStorage.setItem('access_token', result.auth_token)
            this.setState({token: result['text'], loading: false})
        }).then(result => {
            // localStorage.setItem('access_token', result.auth_token)
            console.log(this.state.token)
        }).catch((data) => {
        console.log(`Try again! Error: ${Error(data)}`)
        });
}
    render () {  
        return (
        <Box sx={{  typography: 'body1', margin: "0 auto"}}>
          <form onSubmit={this.handleSubmit}>
          <Stack
           justifyContent="center"
           alignItems="center"
           spacing={2}>
          <TextField sx={{width: '90%'}} id="outlined-basic" label="Введите текст" variant="outlined" onChange={this.handleChange} />
          <LoadingButton
          loading={this.state.loading}
          variant="outlined"
          type='submit'
        >
          Классифицировать
        </LoadingButton>
          {this.state.token?
          <p>{this.state.token}</p> :
          <></>}
          </Stack>
          </form>
        </Box>
      );
    }
}