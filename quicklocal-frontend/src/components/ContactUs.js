import React, { useState } from 'react';
import apiService from '../services/apiService';
import './ContactUs.css';


const ContactUs = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(null);
    
        try {
            await apiService.sendMessage({ name, email, message });
            setSuccess('Your message has been sent successfully!');
            setName('');
            setEmail('');
            setMessage('');
        } catch (err) {
            setError('Failed to send message. Please try again later.');
        } finally {
            setLoading(false);
        }
    };    

    return (
        <div className="contact-us container my-5">
        <div className="row">
            <div className="col-md-5 contact-info">
                <h2 className='my-5 contact-title'>Contact Us <span>QuickLocal</span></h2>
                <p className='contact-par'>
                    Have any questions or feedback? Drop us a message and we will get back to you as soon as possible.
                </p>
            </div>

            <div className="col-md-6 ms-5">
                {success && <div className="alert alert-success">{success}</div>}
                {error && <div className="alert alert-danger">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="name">Name</label>
                        <input
                            type="text"
                            id="name"
                            className="form-control"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="message">Message</label>
                        <textarea
                            id="message"
                            className="form-control"
                            rows="5"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-custom mb-5 mt-3" disabled={loading}>
                        {loading ? 'Sending...' : 'Send Message'}
                    </button>
                </form>
            </div>
        </div>
</div>
    );
};

export default ContactUs;
