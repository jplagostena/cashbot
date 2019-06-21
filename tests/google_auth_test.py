from unittest.mock import MagicMock

import pytest

from google_sheeter import GoogleAuth


class TestGoogleAuth(object):

    def test_is_authorized_with_credentials_ok(self, mocker):
        username = "username"
        google_authorizer = GoogleAuth(username)

        mock_store = self._build_store_and_credential(invalid=False)

        storage = mocker.patch("google_sheeter.file.Storage", return_value=mock_store, autospec=True)
        # assertamos que la credencial sea valida
        assert google_authorizer.is_authorized();

        # chequeamos que la clase haya sido llamada con el constructor indicado
        storage.assert_called_once_with("tokens/" + username + ".json")

    def test_is_authorized_with_invalid_credentials(self, mocker):
        username = "username"
        google_authorizer = GoogleAuth(username)

        mock_store = self._build_store_and_credential(invalid=True)

        storage = mocker.patch("google_sheeter.file.Storage", return_value=mock_store, autospec=True)
        # assertamos que la credencial sea valida
        assert not google_authorizer.is_authorized();
        # chequeamos que la clase haya sido llamada con el constructor indicado
        storage.assert_called_once_with("tokens/" + username + ".json")

    def test_get_credentials_without_code_and_valid_credentials(self, mocker):
        username = "username"
        google_authorizer = GoogleAuth(username)
        mock_store = self._build_store_and_credential(invalid=False)
        mocker.patch("google_sheeter.file.Storage", return_value=mock_store, autospec=True)
        creds = google_authorizer.get_credential()
        assert creds == mock_store.get()

    @pytest.mark.skip(reason="falla: tengo que seguir investigando el mockeo")
    def test_get_credentials_without_code_and_invalid_credentials(self, mocker):
        username = "username"
        google_authorizer = GoogleAuth(username)

        mock_store = self._build_store_and_credential(invalid=True)
        mocker.patch("google_sheeter.file.Storage", return_value=mock_store, autospec=True)

        mock_client = MagicMock()
        mock_flow = MagicMock()
        auth_url = 'authUrl'
        mock_flow.step1_get_authorize_url.return_value = auth_url
        mock_client.flow_from_clientsecrets.return_value = mock_flow
        mocker.patch("google_sheeter.client", return_value=mock_client, autospec=True)
        credential = google_authorizer.get_credential()

        assert auth_url == credential


    def _build_store_and_credential(self, invalid):
        mock_credential = MagicMock(invalid=invalid)
        mock_store = MagicMock()
        mock_store.get.return_value = mock_credential
        return mock_store













