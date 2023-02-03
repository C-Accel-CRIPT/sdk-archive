Each CRIPT user account is associated with a unique API token. This token tells CRIPT who you are and allows you to interact with CRIPT using the Python SDK.

!!! warning "Token Security"
    Anyone who knows your API token can interact with CRIPT using your account. So you should treat it just like a password and keep it secret. If your API token is exposed to other people, you can generate a new one so that no one who has access to your old token can use it anymore. Use the
    <a href="https://criptapp.org/security/" target="_blank">CRIPT Security Settings page</a>
    to generate a new token.

---

## Getting your API token

To get your API token, visit the <a href="https://criptapp.org/security/" target="_blank">CRIPT Security Settings page</a>. Scroll to the API token section and click the `Copy` button. This will copy your API token so that you can paste it somewhere else.

**Example**

```yaml
API Token: Token 4abc478b25e30766652f76103b978349c4c4b214
```

> Note: The text of some API tokens begins with the word "Token" is part of your API token.

---

## Storing your API token
To keep your API token safe, you should generally avoid using directly it
in Python scripts. Instead, store it as an environment variable.
<a href="https://gargankush.medium.com/storing-api-keys-as-environmental-variable-for-windows-linux-and-mac-and-accessing-it-through-974ba7c5109f" target="_blank">For more information, see this guide</a> to learn how to store your API token as an environment variable. The <a href="../full_tutorial/#connect-to-cript" target="_blank">full CRIPT tutorial</a> provides an example of how your API Token can be imported from an environment variable and used in a Python script
for interacting with CRIPT.

---

## Generating a new token

 If your API token is exposed to other people, you can generate a new one on the <a href="https://criptapp.org/security/" target="_blank">CRIPT Security Settings page</a>. Simply click the `Regenerate API token` button, and a new token will be created. Then copy the new token and paste it wherever you store your token.
