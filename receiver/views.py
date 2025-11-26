from django.http import HttpResponseNotFound, HttpResponseRedirect, FileResponse
from .models import Endpoint, APICall
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])

# View to handle incoming API calls
def receive_api_call(request, path):
    # Retrieve the endpoint based on the provided path
    try:
        endpoint = Endpoint.objects.get(path=path)
    # Check if the endpoint is active
    except Endpoint.DoesNotExist:
        endpoint = None

    # If the endpoint is inactive, return 404
    if endpoint and not endpoint.is_active:
        return HttpResponseNotFound()

    # Collect request data
    payload = request.POST.dict() if request.method == "POST" else request.GET.dict()
    method = request.method
    headers = dict(request.headers)
    query_params = request.GET.dict()
    body = request.body.decode("utf-8", errors="replace") if request.body else None
    user_agent = request.headers.get("User-Agent", "")

    # Calculate referer status BEFORE creating APICall
    referer_status = None
    if endpoint and endpoint.response_type == Endpoint.RESPONSE_REFERER:
        referer = request.META.get("HTTP_REFERER", "").strip()

        # If referer is empty or whitespace, mark as failure immediately
        if not referer:
            print("No referer header found")
            referer_status = False
        else:
            # Normalize referer
            normalized_referer = referer.rstrip("/")
            if "://" in normalized_referer:
                normalized_referer = normalized_referer.split("://")[1]
            if ":" in normalized_referer:
                normalized_referer = normalized_referer.split(":")[0]

            # Normalize expected referer
            normalized_expected = endpoint.response_referer_url.strip().rstrip("/")
            if "://" in normalized_expected:
                normalized_expected = normalized_expected.split("://")[1]
            if ":" in normalized_expected:
                normalized_expected = normalized_expected.split(":")[0]

            print(f"Expected referer: {normalized_expected}")
            print(f"Actual referer: {normalized_referer}")

            referer_status = normalized_referer == normalized_expected
            print(f"Matching: {referer_status}")

    # Create APICall with referer_status
    APICall.objects.create(
        endpoint=endpoint,
        payload=payload,
        remote_ip=request.META.get("REMOTE_ADDR"),
        method=method,
        headers=headers,
        query_params=query_params,
        body=body,
        user_agent=user_agent,
        referer_status=referer_status,
    )

    # Determine response based on endpoint configuration and return appropriate response to client
    if not endpoint:
        return HttpResponseNotFound()

    if (
        endpoint.response_type == Endpoint.RESPONSE_REDIRECT
        and endpoint.response_redirect_url
    ):
        return HttpResponseRedirect(endpoint.response_redirect_url)

    if endpoint.response_type == Endpoint.RESPONSE_IMAGE and endpoint.response_image:
        return FileResponse(endpoint.response_image)

    if endpoint.response_type == Endpoint.RESPONSE_REFERER:
        if referer_status and endpoint.response_image_referer_success:
            return FileResponse(endpoint.response_image_referer_success)
        elif endpoint.response_image_referer_failure:
            return FileResponse(endpoint.response_image_referer_failure)

    return HttpResponseNotFound()
