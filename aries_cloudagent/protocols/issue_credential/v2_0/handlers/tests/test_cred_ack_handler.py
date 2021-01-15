from asynctest import (
    mock as async_mock,
    TestCase as AsyncTestCase,
)

from ......messaging.request_context import RequestContext
from ......messaging.responder import MockResponder
from ......transport.inbound.receipt import MessageReceipt

from ...messages.cred_ack import V20CredAck
from .. import cred_ack_handler as test_module


class TestCredentialAckHandler(AsyncTestCase):
    async def test_called(self):
        request_context = RequestContext.test_context()
        request_context.message_receipt = MessageReceipt()
        request_context.connection_record = async_mock.MagicMock()

        with async_mock.patch.object(
            test_module, "V20CredManager", autospec=True
        ) as mock_cred_mgr:
            mock_cred_mgr.return_value.receive_cred_ack = (
                async_mock.CoroutineMock()
            )
            request_context.message = V20CredAck()
            request_context.connection_ready = True
            handler = test_module.V20CredAckHandler()
            responder = MockResponder()
            await handler.handle(request_context, responder)

        mock_cred_mgr.assert_called_once_with(request_context.profile)
        mock_cred_mgr.return_value.receive_credential_ack.assert_called_once_with(
            request_context.message,
            request_context.connection_record.connection_id,
        )
        assert not responder.messages

    async def test_called_not_ready(self):
        request_context = RequestContext.test_context()
        request_context.message_receipt = MessageReceipt()
        request_context.connection_record = async_mock.MagicMock()

        with async_mock.patch.object(
            test_module, "V20CredManager", autospec=True
        ) as mock_cred_mgr:
            mock_cred_mgr.return_value.receive_cred_ack = (
                async_mock.CoroutineMock()
            )
            request_context.message = V20CredAck()
            request_context.connection_ready = False
            handler = test_module.V20CredAckHandler()
            responder = MockResponder()
            with self.assertRaises(test_module.HandlerException):
                await handler.handle(request_context, responder)

        assert not responder.messages
