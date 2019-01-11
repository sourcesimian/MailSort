.PHONY:

dockeret: .PHONY
	docker build \
		--build-arg http_proxy=${http_proxy} \
		--build-arg https_proxy=${https_proxy} \
		--build-arg no_proxy=${no_proxy} \
		-t sourcesimian/mailsort:1 -f ./dockeret/Dockerfile ./
