# Enable SSL certificate for Eve NG Pro with Ansible and Let's Encrypt

Creating a free SSL certificate for your Eve NG Pro with Ansible and Let's Encrypt is easy. I used the steps below to use Ansible to create and deploy a Let's Encrypt SSL certificate for my Eve NG Pro.

1. Install `cerbot`

```yaml
- name: Install certbot
  ansible.builtin.apt:
    update_cache: true
    cache_valid_time: 300
    state: present
    name: certbot
```

2. Stop Apache

```yaml
    - name: Stop apache2, if running
      ansible.builtin.systemd:
        name: apache2
        state: stopped
```

3. Register email and agree to terms. Then, create a new certificate using `non-interactive` mode.

```yaml
- name: register and agree to certbot TOS (required for non-interactive use)
    ansible.builtin.shell: |
    certbot register --agree-tos --email {{ certbot_email }} --non-interactive

- name: Create Let's encrypt certificate
    shell: |
    certbot certonly --standalone --preferred-challenges http -d {{ certbot_domain }} --non-interactive
```

4. Update Apache configuration

assuming you have a variable `certbot_domain` with the site name defined, the following snippet will update the contents of the `/etc/apache2/sites-enabled/eveng-ssl.conf` to include the new certificate and key.

```yaml
- name: set certificate file and certificate key file values
  become: true
  become_user: root
  replace:
    path: /etc/apache2/sites-enabled/eveng-ssl.conf
    regexp: "{{ item.regexp }}"
    replace: '\1 {{ item.replacement }}'
    backup: true
  loop: "{{ certs }}"
  vars:
    certs:
      - regexp: '(SSLCertificateFile\s+)(.*)$'
        replacement: /etc/letsencrypt/live/{{ certbot_domain }}/fullchain.pem
      - regexp: '(SSLCertificateKeyFile\s+)(.*)$'
        replacement: /etc/letsencrypt/live/{{ certbot_domain }}/privkey.pem
```

5. Restart Apache

```yaml
    - name: restart apache2
      ansible.builtin.systemd:
        name: apache2
        state: restarted
```
